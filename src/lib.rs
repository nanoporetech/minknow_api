//! A Rust implementation of the minknow_api client that supports communicating
//! with a MinKNOW server.
//!
//! For more information on MinKNOW and minknow_api clients, see [the minknow_api
//! python client repository].
use std::collections::HashMap;
use std::{thread, time};

use hyper::{
    client::{HttpConnector, ResponseFuture},
    header::HeaderValue,
    Body, Client, Request as HyperRequest, Response as HyperResponse, Uri,
};

use hyper_openssl::HttpsConnector;
use openssl::{
    ssl::{SslConnector, SslMethod},
    x509::X509,
};

use prost::Message;
use std::{env, error::Error, task::Poll};
use tokio_stream::{self as stream, StreamExt};
use tonic::body::BoxBody;
use tonic::{Request, Status};
use tonic_openssl::ALPN_H2_WIRE;
use tower::Service;

use minknow_api::manager::manager_service_client::ManagerServiceClient as MinKNOWManagerClient;
use minknow_api::manager::{DescribeHostRequest, DescribeHostResponse, FlowCellPositionsRequest};

use minknow_api::protocol::protocol_service_client::ProtocolServiceClient as MinKNOWProtocolClient;

pub mod minknow_api {
    pub mod acquisition {
        tonic::include_proto!("minknow_api.acquisition");
    }

    pub mod analysis_configuration {
        tonic::include_proto!("minknow_api.analysis_configuration");
    }

    pub mod basecaller {
        tonic::include_proto!("minknow_api.basecaller");
    }

    pub mod device {
        tonic::include_proto!("minknow_api.device");
    }

    pub mod instance {
        tonic::include_proto!("minknow_api.instance");
    }

    pub mod manager {
        tonic::include_proto!("minknow_api.manager");
    }

    pub mod protocol {
        tonic::include_proto!("minknow_api.protocol");
    }

    pub mod protocol_settings {
        tonic::include_proto!("minknow_api.protocol_settings");
    }

    pub mod run_until {
        tonic::include_proto!("minknow_api.run_until");
    }
}

// A channel for communicating with MinKNOW that supports TLS
// with self signed certificates and handling of MinKNOW
// auth tokens.
//
// A MinKNOWChannel does not know how to obtain certificates and
// auth tokens, so must be provided with a certificate and auth
// token that is valid for the MinKNOW server listening at the
// provided URI
//
// Once those are provided, a MinKNOWChannel knows how to attach
// them to an outgoing request to the MinKNOW server.
#[derive(Clone, Debug)]
pub struct MinKNOWChannel {
    uri: Uri,
    client: Client<HttpsConnector<HttpConnector>, BoxBody>,
    token: Option<String>,
    pub certificate: Vec<u8>,
}

impl MinKNOWChannel {
    // Create a new MinKNOWChannel that will handle SSL communication with the
    // MinKNOW server using the provided certificate.
    //
    // Note that MinKNOW certificates are self-signed, so tonic_openssl is used for
    // connecting the certificate to requests (rather than rustls which does not
    // support self signed certificates).
    //
    // A MinKNOWChannel created using ::new does not include a MinKNOW local auth
    // token. To include auth tokens with requests using this channel, call
    // set_token prior to making a request.
    //
    // This is the case because a MinKNOWChannel must be used to make a request to retrieve the
    // current MinKNOW local auth token.
    pub async fn new(certificate: Vec<u8>, uri: Uri) -> Result<Self, Box<dyn Error>> {
        let mut http = HttpConnector::new();
        http.enforce_http(false);

        let ca = X509::from_pem(&certificate[..])?;
        let mut connector = SslConnector::builder(SslMethod::tls())?;
        connector.cert_store_mut().add_cert(ca)?;
        connector.set_alpn_protos(ALPN_H2_WIRE)?;

        let mut https = HttpsConnector::with_connector(http, connector)?;
        https.set_callback(|c, _| {
            c.set_verify_hostname(false);
            Ok(())
        });

        let client = Client::builder().http2_only(true).build(https);

        Ok(Self {
            client: client,
            uri: uri,
            certificate: certificate,
            token: None,
        })
    }

    pub fn set_token(&mut self, token: String) {
        self.token = Some(token);
    }
}

impl Service<HyperRequest<BoxBody>> for MinKNOWChannel {
    type Response = HyperResponse<Body>;
    type Error = hyper::Error;
    type Future = ResponseFuture;

    fn poll_ready(&mut self, _: &mut std::task::Context<'_>) -> Poll<Result<(), Self::Error>> {
        Ok(()).into()
    }

    // Make an RPC via this MinKNOW channel and if a token is set on this channel,
    // using the channel base URI for scheme and authority and the request URI
    // for RPC endpoint path.
    //
    // If an auth token is set on the channel, add that auth token to headers of
    // outgoing request.
    fn call(&mut self, mut req: HyperRequest<BoxBody>) -> Self::Future {
        let uri = Uri::builder()
            .scheme(self.uri.scheme().unwrap().clone())
            .authority(self.uri.authority().unwrap().clone())
            .path_and_query(req.uri().path_and_query().unwrap().clone())
            .build()
            .unwrap();

        *req.uri_mut() = uri;

        if !self.token.is_none() {
            req.headers_mut().insert(
                "protocol-auth",
                HeaderValue::from_str(self.token.as_ref().unwrap()).unwrap(),
            );
        }

        self.client.request(req)
    }
}

// A flow cell position.
//
// You should not normally construct this directly, but instead call
// `Manager.flow_cell_positions`. The constructor arguments may change between minor
// releases.
#[derive(Debug)]
pub struct FlowCellPosition {
    host: String,
    token: Option<String>,
    pub description: minknow_api::manager::FlowCellPosition,
}

impl FlowCellPosition {
    // Create a new MinKNOWChannel that will handle SSL communication with this
    // flow cell position.
    async fn channel(&self) -> MinKNOWChannel {
        let cert_path = env::var("MINKNOW_TRUSTED_CA").ok().unwrap();
        let cert = tokio::fs::read(cert_path).await.ok().unwrap();

        let host = self.host.clone();
        println!("{:?}", self.description);
        let port = self.description.rpc_ports.as_ref().unwrap().secure.clone();
        let uri = Uri::from_maybe_shared(format!("https://{host}:{port}")).unwrap();

        let mut channel = MinKNOWChannel::new(cert, uri).await.unwrap();
        if !self.token.is_none() {
            channel.set_token(self.token.as_ref().unwrap().clone())
        }

        return channel;
    }
}

pub struct Protocol {
    pub channel: MinKNOWChannel,
}

impl Protocol {
    // Initiates a python instance that run the script specified by the 'identifier' argument.
    // `list_protocols` will give back a list of protocol scripts that can be started by this
    // call.
    async fn start_protocol(
        &self,
        identifier: String,
        args: Vec<String>,
        user_info: Option<minknow_api::protocol::ProtocolRunUserInfo>,
        offload_location_info: Option<minknow_api::protocol::OffloadLocationInfo>,
        target_run_until_criteria: Option<minknow_api::acquisition::TargetRunUntilCriteria>,
    ) -> Result<minknow_api::protocol::StartProtocolResponse, Status> {
        let channel = self.channel.clone();

        let mut client = MinKNOWProtocolClient::new(channel);
        let request = Request::new(minknow_api::protocol::StartProtocolRequest {
            identifier,
            args,
            user_info,
            offload_location_info,
            target_run_until_criteria,
        });

        let response = match client.start_protocol(request).await {
            Ok(response) => response.into_inner(),
            Err(err) => return Err(Status::unavailable("Not available")),
        };

        Ok(response)
    }

    // Wait for a protocol run to finish.
    //
    // This call blocks until the run with the given run ID has finished (or returns immediately
    // if it had already finished) and returns information about the protocol run.
    //
    // If no run has been started with the provided run ID (or no run ID is given), and error is
    // returned.
    //
    // If NOTIFY_BEFORE_TERMINATION is specified for state, the protocol end time is an estimate,
    // including the the allowed timeout.
    async fn wait_for_finished(
        &self,
        run_id: String,
        state: Option<minknow_api::protocol::wait_for_finished_request::NotificationState>,
        timeout: f32,
    ) -> Result<minknow_api::protocol::ProtocolRunInfo, Status> {
        let channel = self.channel.clone();

        let mut client = MinKNOWProtocolClient::new(channel);

        let request_state = match state {
            Some(state) => state as i32,
            None => minknow_api::protocol::wait_for_finished_request::NotificationState::NotifyOnTermination as i32
        };

        let request = Request::new(minknow_api::protocol::WaitForFinishedRequest {
            run_id: run_id,
            state: request_state,
            timeout: timeout,
        });

        let response = match client.wait_for_finished(request).await {
            Ok(response) => response.into_inner(),
            Err(err) => return Err(Status::unavailable("Not available")),
        };

        Ok(response)
    }
}

// A connection to the manager gRPC interface.
#[derive(Debug)]
pub struct Manager {
    pub channel: MinKNOWChannel,
}

impl Manager {
    // Create a new Manager instance by creating a MinKNOWChannel over which
    // requests can be forwarded to the MinKNOW server.
    //
    // This includes using the `MINKNOW_TRUSTED_CA` environment variable to find and
    // provide the client certificate for encrypted communication with the MinKNOW
    // server
    //
    // More information on secure communication with the MinKNOW server can be found
    // here: https://github.com/nanoporetech/minknow_api#faqs
    async fn new(host: String, port: u32) -> Manager {
        let cert_path = env::var("MINKNOW_TRUSTED_CA").ok().unwrap();
        let cert = tokio::fs::read(cert_path).await.ok().unwrap();
        let uri = Uri::from_maybe_shared(format!("https://{host}:{port}")).unwrap();

        let channel = MinKNOWChannel::new(cert, uri).await.unwrap();
        Self { channel: channel }
    }

    // Get information about the machine running MinKNOW.
    async fn describe_host(&self) -> Result<DescribeHostResponse, Status> {
        let channel = self.channel.clone();

        let mut client = MinKNOWManagerClient::new(channel);
        let request = Request::new(DescribeHostRequest {});

        let response = match client.describe_host(request).await {
            Ok(response) => response.into_inner(),
            Err(err) => return Err(Status::unavailable("Not available")),
        };

        Ok(response)
    }

    // Get a list of flow cell positions.
    async fn flow_cell_positions(&self) -> Result<Vec<FlowCellPosition>, Status> {
        let channel = self.channel.clone();
        let token = channel.token.clone();

        let mut client = MinKNOWManagerClient::new(channel);
        let request = Request::new(FlowCellPositionsRequest {});

        let response = match client.flow_cell_positions(request).await {
            Ok(response) => response.into_inner(),
            Err(err) => return Err(Status::unavailable("Not available")),
        };

        let flow_cells = response
            .fold(Vec::new(), |acc, result| {
                [acc, result.unwrap().positions].concat()
            })
            .await
            .into_iter()
            .map(|position| FlowCellPosition {
                host: "localhost".to_string(),
                token: token.clone(),
                description: position,
            })
            .collect::<Vec<FlowCellPosition>>();

        Ok(flow_cells)
    }

    // Dynamically create a simulated device
    async fn add_simulated_device(
        &self,
        name: String,
        simulated_type: minknow_api::manager::SimulatedDeviceType,
    ) -> Result<minknow_api::manager::AddSimulatedDeviceResponse, Status> {
        let channel = self.channel.clone();

        let mut client = MinKNOWManagerClient::new(channel);
        let request = Request::new(minknow_api::manager::AddSimulatedDeviceRequest {
            name,
            r#type: simulated_type as i32,
        });

        let response = match client.add_simulated_device(request).await {
            Ok(response) => response.into_inner(),
            Err(err) => {
                println!("{:?}", err);
                return Err(Status::unavailable("Not available"));
            }
        };

        Ok(response)
    }

    // Dynamically remove a simulated device
    async fn remove_simulated_device(
        &self,
        name: String,
    ) -> Result<minknow_api::manager::RemoveSimulatedDeviceResponse, Status> {
        let channel = self.channel.clone();

        let mut client = MinKNOWManagerClient::new(channel);
        let request = Request::new(minknow_api::manager::RemoveSimulatedDeviceRequest { name });

        let response = match client.remove_simulated_device(request).await {
            Ok(response) => response.into_inner(),
            Err(err) => {
                println!("{:?}", err);
                return Err(Status::unavailable("Not available"));
            }
        };

        Ok(response)
    }

    // Reset a flow cell position.
    async fn reset_position(
        &self,
        position: String,
        force: bool,
    ) -> Result<minknow_api::manager::ResetPositionResponse, Status> {
        self.reset_positions(vec![position], force).await
    }

    // Reset flow cell positions.
    async fn reset_positions(
        &self,
        positions: Vec<String>,
        force: bool,
    ) -> Result<minknow_api::manager::ResetPositionResponse, Status> {
        let channel = self.channel.clone();

        let mut client = MinKNOWManagerClient::new(channel);
        let request = Request::new(minknow_api::manager::ResetPositionRequest { positions, force });

        let response = match client.reset_position(request).await {
            Ok(response) => response.into_inner(),
            Err(err) => {
                println!("{:?}", err);
                return Err(Status::unavailable("Not available"));
            }
        };

        Ok(response)
    }

    // Create a new developer api token, which expires at [expiry]
    //
    // Cannot be invoked when using a developer token as authorisation method.
    async fn create_developer_api_token(
        &self,
        name: String,
    ) -> Result<minknow_api::manager::CreateDeveloperApiTokenResponse, Status> {
        let channel = self.channel.clone();

        let mut client = MinKNOWManagerClient::new(channel);
        let request = Request::new(minknow_api::manager::CreateDeveloperApiTokenRequest {
            name,
            expiry: None,
        });

        let response = match client.create_developer_api_token(request).await {
            Ok(response) => response.into_inner(),
            Err(err) => {
                println!("{:?}", err);
                return Err(Status::unavailable("Not available"));
            }
        };

        Ok(response)
    }

    // Revoke an existing developer API token.
    async fn revoke_developer_api_token(
        &self,
        id: String,
    ) -> Result<minknow_api::manager::RevokeDeveloperApiTokensResponse, Status> {
        let channel = self.channel.clone();

        let mut client = MinKNOWManagerClient::new(channel);
        let request = Request::new(minknow_api::manager::RevokeDeveloperApiTokenRequest { id });

        let response = match client.revoke_developer_api_token(request).await {
            Ok(response) => response.into_inner(),
            Err(err) => {
                println!("{:?}", err);
                return Err(Status::unavailable("Not available"));
            }
        };

        Ok(response)
    }

    // List existing developer API tokens.
    async fn list_developer_api_tokens(
        &self,
    ) -> Result<minknow_api::manager::ListDeveloperApiTokensResponse, Status> {
        let channel = self.channel.clone();

        let mut client = MinKNOWManagerClient::new(channel);
        let request = Request::new(minknow_api::manager::ListDeveloperApiTokensRequest {});

        let response = match client.list_developer_api_tokens(request).await {
            Ok(response) => response.into_inner(),
            Err(err) => {
                println!("{:?}", err);
                return Err(Status::unavailable("Not available"));
            }
        };

        Ok(response)
    }

    // List available protocols for the given experiment type.
    async fn find_protocols(
        &self,
        experiment_type: minknow_api::manager::ExperimentType,
    ) -> Result<minknow_api::manager::FindProtocolsResponse, Status> {
        let channel = self.channel.clone();

        let mut client = MinKNOWManagerClient::new(channel);
        let request = Request::new(minknow_api::manager::FindProtocolsRequest {
            experiment_type: experiment_type as i32,
            flow_cell_product_code: String::default(),
            sequencing_kit: String::default(),
        });

        let response = match client.find_protocols(request).await {
            Ok(response) => response.into_inner(),
            Err(err) => {
                println!("{:?}", err);
                return Err(Status::unavailable("Not available"));
            }
        };

        Ok(response)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test]
    async fn test_describe_host() {
        let manager = Manager::new("localhost".to_string(), 9502).await;

        let response = manager.describe_host().await;
        assert!(response.is_ok());
    }

    #[tokio::test]
    async fn test_developer_api_token_management() {
        let mut manager = Manager::new("localhost".to_string(), 9502).await;

        let test_base_token = env::var("MINKNOW_API_TEST_TOKEN").ok().unwrap();
        manager.channel.set_token(test_base_token);

        let response = manager
            .create_developer_api_token("test_developer_api_token_management".to_string())
            .await;

        assert!(response.is_ok());

        let unwrapped_response = &response.unwrap();
        let id = unwrapped_response.id.clone();

        let response = manager.list_developer_api_tokens().await;
        assert!(response.is_ok());

        let response = manager.revoke_developer_api_token(id).await;
        assert!(response.is_ok());
    }

    #[tokio::test]
    async fn test_find_protocols() {
        let mut manager = Manager::new("localhost".to_string(), 9502).await;

        let test_base_token = env::var("MINKNOW_API_TEST_TOKEN").ok().unwrap();
        manager.channel.set_token(test_base_token);

        let response = manager
            .find_protocols(minknow_api::manager::ExperimentType::AllIncludingHidden)
            .await;

        assert!(response.is_ok());

        println!("{:?}", &response.unwrap().protocols.clone());
    }

    #[tokio::test]
    async fn test_simulated_minion_e2e() {
        let device_name = "MS12345".to_string();
        let mut manager = Manager::new("localhost".to_string(), 9502).await;

        let test_base_token = env::var("MINKNOW_API_TEST_TOKEN").ok().unwrap();
        manager.channel.set_token(test_base_token);

        let response = manager
            .create_developer_api_token("test_simulated_minion_end_to_end".to_string())
            .await;

        assert!(response.is_ok());

        let unwrapped_response = &response.unwrap();
        let token = unwrapped_response.token.clone();
        let id = unwrapped_response.id.clone();

        manager.channel.set_token(token);

        let response = manager
            .add_simulated_device(
                device_name.clone(),
                minknow_api::manager::SimulatedDeviceType::SimulatedMinion,
            )
            .await;

        assert!(response.is_ok());

        let five_secs = time::Duration::from_secs(5);
        thread::sleep(five_secs);

        let response = manager.flow_cell_positions().await;
        let potentially_found_flow_cell = response
            .unwrap()
            .into_iter()
            .find(|position| position.description.name == device_name.clone());

        let found_flow_cell = match potentially_found_flow_cell {
            Some(found_flow_cell) => found_flow_cell,
            None => panic!("Could not find flow cell"),
        };

        let channel = found_flow_cell.channel().await;

        let protocol = Protocol { channel };
        let response = protocol
            .start_protocol(
                "checks/flowcell_check/platform_qc:FLO-MIN106".to_string(),
                Vec::new(),
                None,
                None,
                None,
            )
            .await;
        assert!(response.is_ok());

        let unwrapped_response = &response.unwrap();
        let run_id = unwrapped_response.run_id.clone();
        let response = protocol.wait_for_finished(run_id, None, 10000.0).await;
        assert!(response.is_ok());

        let response = manager.remove_simulated_device(device_name.clone()).await;
        assert!(response.is_ok());

        let response = manager.reset_position(device_name.clone(), false).await;
        assert!(response.is_ok());

        let response = manager.revoke_developer_api_token(id).await;
        assert!(response.is_ok());
    }

    #[tokio::test]
    async fn test_simulated_promethion_e2e() {
        let device_name = "P2S_00007-1".to_string();

        let mut manager = Manager::new("localhost".to_string(), 9502).await;

        let test_base_token = env::var("MINKNOW_API_TEST_TOKEN").ok().unwrap();
        manager.channel.set_token(test_base_token);

        let response = manager
            .create_developer_api_token("test_simulated_promethion_end_to_end".to_string())
            .await;

        assert!(response.is_ok());

        let unwrapped_response = &response.unwrap();
        let token = unwrapped_response.token.clone();
        let id = unwrapped_response.id.clone();

        manager.channel.set_token(token);

        let response = manager
            .add_simulated_device(
                device_name.clone(),
                minknow_api::manager::SimulatedDeviceType::SimulatedPromethion,
            )
            .await;

        assert!(response.is_ok());

        let five_secs = time::Duration::from_secs(5);
        thread::sleep(five_secs);

        let response = manager.flow_cell_positions().await;

        let potentially_found_flow_cell = response
            .unwrap()
            .into_iter()
            .find(|position| position.description.name == device_name.clone());

        let found_flow_cell = match potentially_found_flow_cell {
            Some(found_flow_cell) => found_flow_cell,
            None => panic!("Could not find flow cell"),
        };

        let channel = found_flow_cell.channel().await;

        let protocol = Protocol { channel };
        let response = protocol
            .start_protocol(
                "checks/flowcell_check/platform_qc:FLO-PRO002".to_string(),
                Vec::new(),
                None,
                None,
                None,
            )
            .await;
        assert!(response.is_ok());

        let unwrapped_response = &response.unwrap();
        let run_id = unwrapped_response.run_id.clone();
        let response = protocol.wait_for_finished(run_id, None, 10000.0).await;
        assert!(response.is_ok());

        let mut stop_after_60_secs = HashMap::new();
        let int_type_60_secs = prost_types::Value {
            kind: Some(prost_types::value::Kind::NumberValue(60.0)),
        };

        stop_after_60_secs.insert(
            String::from("runtime"),
            prost_types::Any {
                type_url: String::from("type.googleapis.com/google.protobuf.Int64Value"),
                value: int_type_60_secs.encode_to_vec(),
            },
        );

        let response = protocol
            .start_protocol(
                "sequencing/sequencing_PRO002_DNA:FLO-PRO002:SQK-LSK110".to_string(),
                Vec::new(),
                None,
                None,
                Some(minknow_api::acquisition::TargetRunUntilCriteria {
                    pause_criteria: None,
                    stop_criteria: Some(minknow_api::run_until::CriteriaValues {
                        criteria: stop_after_60_secs,
                    }),
                }),
            )
            .await;
        assert!(response.is_ok());

        let unwrapped_response = &response.unwrap();
        let run_id = unwrapped_response.run_id.clone();
        let response = protocol.wait_for_finished(run_id, None, 10000.0).await;
        assert!(response.is_ok());

        let response = manager.remove_simulated_device(device_name.clone()).await;
        assert!(response.is_ok());

        let response = manager.reset_position(device_name.clone(), false).await;
        assert!(response.is_ok());

        let response = manager.revoke_developer_api_token(id).await;
        assert!(response.is_ok());
    }
}
