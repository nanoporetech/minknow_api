This section of the API is an under-construction replacement of the per-flow-cell-position APIs, such as:

## ProtocolService
* list_protocol_runs
* get_run_info
* generate_run_report
* clear_protocol_history_data

## AcquisitionService
* get_acquisition_info
* list_acquisition_runs

The above calls should be made to the usual manager port (9501/2) rather than to individual `control_server` ports.
Each of the above calls will be modified to add a `run_id` field, or potentially a 'repeated' `run_id` for interacting with multiple protocols simultaneously.
