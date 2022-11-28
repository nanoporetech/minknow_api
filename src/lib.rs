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

use std::{error::Error, task::Poll, env};
use tonic::body::BoxBody;
use tonic_openssl::ALPN_H2_WIRE;
use tonic::{Request, Status};
use tower::Service;
use tokio_stream::StreamExt;

use minknow_api::manager::manager_service_client::ManagerServiceClient as MinKNOWManagerClient;
use minknow_api::manager::{DescribeHostRequest, DescribeHostResponse, FlowCellPositionsRequest};

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

// A flow cell position
//
// You should not normally construct this directly, but instead call
// `Manager.flow_cell_positions`. The constructor arguments may change between minor
// releases.
#[derive(Clone, Debug)]
pub struct FlowCellPosition {
    name: String
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
    pub certificate: Vec<u8>
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

    fn poll_ready(&mut self, _: & mut std::task::Context<'_>) -> Poll<Result<(), Self::Error>> {
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

// A connection to the manager gRPC interface.
#[derive(Debug)]
pub struct Manager {
    pub channel: MinKNOWChannel
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
        let uri = Uri::from_maybe_shared(format!("https://{host}:{port}"))
            .unwrap();

        let channel = MinKNOWChannel::new(cert, uri).await.unwrap();
        Self {
            channel: channel
        }
    }

    // Get information about the machine running MinKNOW.
    async fn describe_host(&self) -> Result<DescribeHostResponse, Status> {
        let channel = self.channel.clone();

        let mut client = MinKNOWManagerClient::new(channel);
        let request = Request::new(DescribeHostRequest {});

        let response = match client.describe_host(request).await {
            Ok(response) => response.into_inner(),
            Err(err) => {
                return Err(Status::unavailable("Not available"))
            }
        };

        Ok(response)
    }

    // Get a list of flow cell positions.
    async fn flow_cell_positions(&self) -> Result<Vec<FlowCellPosition>, Status> {
        let channel = self.channel.clone();

        let mut client = MinKNOWManagerClient::new(channel);
        let request = Request::new(FlowCellPositionsRequest {});

        let response = match client.flow_cell_positions(request).await {
            Ok(response) => response.into_inner(),
            Err(err) => {
                return Err(Status::unavailable("Not available"))
            }
        };

        let flow_cells = response
            .fold(Vec::new(), |acc, result| {
                [acc, result.unwrap().positions].concat()
            })
            .await
            .into_iter()
            .map(|position| {
                FlowCellPosition {
                    name: position.name.clone()
                }
            })
            .collect::<Vec<FlowCellPosition>>();

        Ok(flow_cells)
    }

    // Dynamically create a simulated device
    async fn add_simulated_device(
        &self,
        name: String,
        simulated_type: minknow_api::manager::SimulatedDeviceType
    ) -> Result<minknow_api::manager::AddSimulatedDeviceResponse, Status> {
        let channel = self.channel.clone();

        let mut client = MinKNOWManagerClient::new(channel);
        let request = Request::new(
            minknow_api::manager::AddSimulatedDeviceRequest {
                name,
                r#type: simulated_type as i32,
            }
        );

        let response = match client.add_simulated_device(request).await {
            Ok(response) => response.into_inner(),
            Err(err) => {
                println!("{:?}", err);
                return Err(Status::unavailable("Not available"))
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
        let request = Request::new(
            minknow_api::manager::RemoveSimulatedDeviceRequest {
                name,
            }
        );

        let response = match client.remove_simulated_device(request).await {
            Ok(response) => response.into_inner(),
            Err(err) => {
                println!("{:?}", err);
                return Err(Status::unavailable("Not available"))
            }
        };

        Ok(response)
    }

    // Reset a flow cell position.
    async fn reset_position(
        &self,
        position: String,
        force: bool
    ) -> Result<minknow_api::manager::ResetPositionResponse, Status> {
        self.reset_positions(vec![position], force).await
    }

    async fn reset_positions(
        &self,
        positions: Vec<String>,
        force: bool
    ) -> Result<minknow_api::manager::ResetPositionResponse, Status> {
        let channel = self.channel.clone();

        let mut client = MinKNOWManagerClient::new(channel);
        let request = Request::new(
            minknow_api::manager::ResetPositionRequest {
                positions,
                force
            }
        );

        let response = match client.reset_position(request).await {
            Ok(response) => response.into_inner(),
            Err(err) => {
                println!("{:?}", err);
                return Err(Status::unavailable("Not available"))
            }
        };

        Ok(response)
    }

    async fn create_developer_api_token(
        &self,
        name: String
    ) -> Result<minknow_api::manager::CreateDeveloperApiTokenResponse, Status> {
        let channel = self.channel.clone();

        let mut client = MinKNOWManagerClient::new(channel);
        let request = Request::new(
            minknow_api::manager::CreateDeveloperApiTokenRequest {
                name,
                expiry: None
            }
        );

        let response = match client.create_developer_api_token(request).await {
            Ok(response) => response.into_inner(),
            Err(err) => {
                println!("{:?}", err);
                return Err(Status::unavailable("Not available"))
            }
        };

        Ok(response)
    }    

    async fn revoke_developer_api_token(
        &self,
        id: String
    ) -> Result<minknow_api::manager::RevokeDeveloperApiTokensResponse, Status> {
        let channel = self.channel.clone();

        let mut client = MinKNOWManagerClient::new(channel);
        let request = Request::new(
            minknow_api::manager::RevokeDeveloperApiTokenRequest {
                id
            }
        );

        let response = match client.revoke_developer_api_token(request).await {
            Ok(response) => response.into_inner(),
            Err(err) => {
                println!("{:?}", err);
                return Err(Status::unavailable("Not available"))
            }
        };

        Ok(response)
    }    

    async fn list_developer_api_tokens(
        &self
    ) -> Result<minknow_api::manager::ListDeveloperApiTokensResponse, Status> {
        let channel = self.channel.clone();

        let mut client = MinKNOWManagerClient::new(channel);
        let request = Request::new(
            minknow_api::manager::ListDeveloperApiTokensRequest {}
        );

        let response = match client.list_developer_api_tokens(request).await {
            Ok(response) => response.into_inner(),
            Err(err) => {
                println!("{:?}", err);
                return Err(Status::unavailable("Not available"))
            }
        };

        Ok(response)
    }    

    async fn find_protocols(
        &self,
        experiment_type: minknow_api::manager::ExperimentType
    ) -> Result<minknow_api::manager::FindProtocolsResponse, Status> {
        let channel = self.channel.clone();

        let mut client = MinKNOWManagerClient::new(channel);
        let request = Request::new(
            minknow_api::manager::FindProtocolsRequest {
                experiment_type: experiment_type as i32,
                flow_cell_product_code: String::default(),
                sequencing_kit: String::default()
            }
        );

        let response = match client.find_protocols(request).await {
            Ok(response) => response.into_inner(),
            Err(err) => {
                println!("{:?}", err);
                return Err(Status::unavailable("Not available"))
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
        let manager = Manager::new(
            "localhost".to_string(),
            9502
        ).await;

        let response = manager.describe_host().await;
        assert!(response.is_ok());
    }

    #[tokio::test]
    async fn test_simulated_device_end_to_end() {
        let mut manager = Manager::new(
            "localhost".to_string(),
            9502
        ).await;
        
        manager.channel.set_token("5bd16355-3e52-4be0-8462-23eda1fb3c06".to_string());

        let response = manager.create_developer_api_token(
            "test_simulated_end_to_end".to_string()
        ).await;

        assert!(response.is_ok());

        let unwrapped_response = &response.unwrap();
        let token = unwrapped_response.token.clone();
        let id = unwrapped_response.id.clone();

        manager.channel.set_token(token);

        let response = manager.add_simulated_device(
          "MS12345".to_string(),
          minknow_api::manager::SimulatedDeviceType::SimulatedMinion
        ).await;

        assert!(response.is_ok());

        let response = manager.flow_cell_positions().await;
        assert!(response.is_ok());

        let flow_cell_positions = response.unwrap();
        assert_eq!(flow_cell_positions.len(), 1);

        let response = manager.remove_simulated_device("MS12345".to_string()).await;
        assert!(response.is_ok());

        let position_name = &flow_cell_positions[0].name;
        let response = manager.reset_position("MS12345".to_string(), false).await;
        assert!(response.is_ok());

        let response = manager.revoke_developer_api_token(id).await;
        assert!(response.is_ok());
    }

    #[tokio::test]
    async fn test_developer_api_token_management() {
        let mut manager = Manager::new(
            "localhost".to_string(),
            9502
        ).await;
        
        manager.channel.set_token("5bd16355-3e52-4be0-8462-23eda1fb3c06".to_string());

        let response = manager.create_developer_api_token(
            "test_developer_api_token_management".to_string()
        ).await;

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
        let mut manager = Manager::new(
            "localhost".to_string(),
            9502
        ).await;
        
        manager.channel.set_token("5bd16355-3e52-4be0-8462-23eda1fb3c06".to_string());

        let response = manager.find_protocols(
            minknow_api::manager::ExperimentType::Sequencing
        ).await;

        assert!(response.is_ok());
    }
}
