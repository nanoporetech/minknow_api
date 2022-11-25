#[macro_use]
extern crate lazy_static;

use prost_types::Timestamp;
use std::sync::Mutex;
use std::{thread, time};
use tokio::net::TcpListener;
use tokio::sync::mpsc;
use tokio_stream::wrappers::ReceiverStream;
use tonic::{transport::Server, Request, Response, Status};

use openssl::ssl::{select_next_proto, AlpnError, SslAcceptor, SslFiletype, SslMethod};
use tokio_stream::wrappers::TcpListenerStream;
use tonic_openssl::ALPN_H2_WIRE;

use minknow_api::manager::{DescribeHostRequest, DescribeHostResponse};

use minknow_api::manager::manager_service_server::{
    ManagerService as Manager, ManagerServiceServer as ManagerServer,
};

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

#[derive(Debug, Default, Clone)]
pub struct MockFlowCellPosition {
    pub name: String,
    pub state: minknow_api::manager::flow_cell_position::State,
    pub protocol_server_port: u32,
    pub total_pore_count: u32,
}

#[derive(Debug, Default)]
pub struct MockMinKNOWManager {
    mock_flow_cell_positions: Vec<MockFlowCellPosition>,
}

#[tonic::async_trait]
impl Manager for MockMinKNOWManager {
    async fn describe_host(
        &self,
        request: tonic::Request<minknow_api::manager::DescribeHostRequest>,
    ) -> Result<tonic::Response<minknow_api::manager::DescribeHostResponse>, tonic::Status> {
        Ok(
            tonic::Response::new(minknow_api::manager::DescribeHostResponse {
                can_sequence_offline: bool::default(),
                description: String::default(),
                network_name: String::default(),
                serial: String::default(),
                product_code: String::default(),
                needs_association: bool::default()
            })
        )
    }

    type flow_cell_positionsStream = ReceiverStream<Result<minknow_api::manager::FlowCellPositionsResponse, Status>>;

    async fn flow_cell_positions(
        &self,
        request: Request<minknow_api::manager::FlowCellPositionsRequest>,
    ) -> Result<Response<Self::flow_cell_positionsStream>, Status> {
        println!("Received request: {:?}", request);

        let (tx, rx) = mpsc::channel(1);

        let positions: Vec<minknow_api::manager::FlowCellPosition> = self
            .mock_flow_cell_positions
            .clone()
            .into_iter()
            .map(|position| {
                minknow_api::manager::FlowCellPosition {
                    name: position.name.clone(),
                    location: None,
                    rpc_ports: None,
                    state: position.state as i32,
                    error_info: String::default(),
                    shared_hardware_group: None,
                    is_integrated: bool::default(),
                    can_sequence_offline: bool::default(),
                    device_type: i32::default(),
                    is_simulated: bool::default(),
                    parent_name: String::default(),
                    protocol_state: i32::default()
                }
            })
            .collect();

        let response = minknow_api::manager::FlowCellPositionsResponse {
            total_count: positions.len() as i32,
            positions: positions,
        };

        tx.send(Ok(response)).await.unwrap();

        Ok(Response::new(ReceiverStream::new(rx)))
    }

    async fn local_authentication_token_path(
        &self,
        _request: tonic::Request<minknow_api::manager::LocalAuthenticationTokenPathRequest>,
    ) -> Result<tonic::Response<minknow_api::manager::LocalAuthenticationTokenPathResponse>, tonic::Status>
    {
        let path = "mock_fixtures/auth.json".to_string();
        Ok(Response::new(
            minknow_api::manager::LocalAuthenticationTokenPathResponse { path },
        ))
    }
}

lazy_static! {
    static ref AVAILABLE_PORT: Mutex<u32> = Mutex::new(9600);
}

pub struct MockManagerServer {
    pub port: u32,
    mock_flow_cell_positions: Vec<MockFlowCellPosition>,
}

pub fn get_available_port() -> u32 {
    let mut port = AVAILABLE_PORT.lock().unwrap();
    let return_port = *port;
    *port += 1;
    return return_port;
}

impl MockManagerServer {
    pub fn new(mock_flow_cell_positions: Vec<MockFlowCellPosition>) -> MockManagerServer {
        let manager_server = MockManagerServer {
            port: get_available_port(),
            mock_flow_cell_positions: mock_flow_cell_positions,
        };

        return manager_server;
    }

    pub async fn start_in_background(&self) -> tokio::task::JoinHandle<()> {
        let mut acceptor = SslAcceptor::mozilla_intermediate(SslMethod::tls()).unwrap();
        acceptor
            .set_private_key_file("mock_fixtures/localhost.key", SslFiletype::PEM)
            .unwrap();

        acceptor
            .set_certificate_chain_file("mock_fixtures/ca.crt")
            .unwrap();

        acceptor.check_private_key().unwrap();
        acceptor.set_alpn_protos(ALPN_H2_WIRE);
        acceptor.set_alpn_select_callback(|_ssl, alpn| {
            select_next_proto(ALPN_H2_WIRE, alpn).ok_or(AlpnError::NOACK)
        });

        let acceptor = acceptor.build();

        let port = self.port;
        let listener = TcpListener::bind(format!("localhost:{port}")).await.unwrap();
        let incoming: tonic_openssl::SslStream<tokio::net::TcpStream> = tonic_openssl::incoming(TcpListenerStream::new(listener), acceptor);

        let manager = MockMinKNOWManager {
            mock_flow_cell_positions: self.mock_flow_cell_positions.clone(),
        };

        tokio::spawn(async move {
            Server::builder()
                .add_service(ManagerServer::new(manager))
                .serve_with_incoming(incoming)
                .await
                .unwrap();
        })
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use tokio_stream::StreamExt;

    #[tokio::test]
    async fn flow_cell_positions() {
        let flow_cell_position_name_1 = "MN12345".to_string();
        let flow_cell_position_name_2 = "MN54678".to_string();

        let flow_cell_position_1 = MockFlowCellPosition {
            name: flow_cell_position_name_1.clone(),
            state: State::Running,
            protocol_server_port: get_available_port(),
            total_pore_count: 300,
        };

        let flow_cell_position_2 = MockFlowCellPosition {
            name: flow_cell_position_name_2.clone(),
            state: State::Initialising,
            protocol_server_port: get_available_port(),
            total_pore_count: 300,
        };

        let manager = MockMinKNOWManager {
            mock_flow_cell_positions: vec![flow_cell_position_1, flow_cell_position_2],
        };

        let request = Request::new(FlowCellPositionsRequest {});
        let response = manager.flow_cell_positions(request).await;

        assert!(response.is_ok());

        let responses: Vec<FlowCellPositionsResponse> = response
            .unwrap()
            .into_inner()
            .map(|result| result.unwrap())
            .collect()
            .await;

        assert_eq!(responses.len(), 1);

        let flow_cell_position_response_1 = &responses[0];
        assert_eq!(flow_cell_position_response_1.total_count, 2);

        let received_flow_cell_position_1 = &flow_cell_position_response_1.positions[0];
        assert_eq!(
            received_flow_cell_position_1.name,
            flow_cell_position_name_1
        );

        let received_flow_cell_position_2 = &flow_cell_position_response_1.positions[1];
        assert_eq!(
            received_flow_cell_position_2.name,
            flow_cell_position_name_2
        );
    }
}
