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
use tonic::{transport::Server, Request, Status};
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

#[derive(Clone, Debug)]
pub struct FlowCellPosition {
    name: String
}

#[derive(Clone, Debug)]
pub struct MinKNOWChannel {
    uri: Uri,
    client: Client<HttpsConnector<HttpConnector>, BoxBody>,
    token: Option<String>,
    pub certificate: Vec<u8>
}

impl MinKNOWChannel {
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

#[derive(Debug)]
pub struct Manager {
    channel: MinKNOWChannel
}

impl Manager {
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
    async fn test_flow_cell_positions() {
        let manager = Manager::new(
            "localhost".to_string(),
            9502
        ).await;

        let response = manager.flow_cell_positions().await;
        assert!(response.is_ok());

        let flow_cell_positions = response.unwrap();
        assert_eq!(flow_cell_positions.len(), 0);
    }
}
