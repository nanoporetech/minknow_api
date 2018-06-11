#-------------------------------------------------------------------------------
# This example will show you how to start a protocol in minknow using the
# gRPC api.
#
# You need to have python 3 installed on your machine
# 
# Python needs the grpc libraries installed in order to talk to MinKNOW:
#
# > pip install protobuf grpcio grpcio-tools
# 
# > mkdir ./examples/generated/
# > python -m grpc_tools.protoc \
#       --python_out=./examples/generated/ \        # Protobuf output dir
#       --grpc_python_out=./examples/generated/ \   # grpc output dir
#       -I . \                                      # Include path for protobuf
#       minknow/rpc/*.proto                         # Protobuf source files
#
# Now the ./examples/generated/ folder contains minknow's api generated for
# python3.
#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
# Now python can import the generated api:
#
# First we add the directory we generated into to the python path
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "generated")) 

# Then import the generated api
import minknow.rpc.protocol_pb2 as protocol
import minknow.rpc.protocol_pb2_grpc as protocol_grpc

# Import the grpc libraries we installed earlier
import grpc
from google.protobuf.wrappers_pb2 import StringValue
#-------------------------------------------------------------------------------


# Define a utility to search for a protocol in the list of returned protocols:
def find_protocol(protocols, flow_cell, kit, experiment_type):
    def has_tag(protocol, tag_name, tag_value):
        # Search each tag to find if it matches the requested tag
        for tag in protocol.tags:
            if (tag == tag_name and protocol.tags[tag].string_value == tag_value):
                return True
        return False

    # Search all protocols to find the one with matching flow cell and kit
    for protocol in protocols.protocols:
        if (has_tag(protocol, "flow cell", flow_cell) and
            has_tag(protocol, "kit", kit) and
            has_tag(protocol, "experiment type", "sequencing")):
            return protocol

    # Potentially an invalid script combination was requested?
    raise Exception("Protocol %s %s %s not found!" % (flow_cell, kit, experiment_type))

#-------------------------------------------------------------------------------
# Connect to the running MinKNOW instance:
# 
# We can connect to a running MinKNOW instance on the local computer (ports may
# vary depending on setup)
#
channel = grpc.insecure_channel('minicol560:8004')
stub = protocol_grpc.ProtocolServiceStub(channel)
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# Find the protocols available on the running MinKNOW instance:
#
print("Listing protocols:")

# Construct a list message to send to MinKNOW
list_request = protocol.ListProtocolsRequest()
# Send the message to MinKNOW and wait for a response
available_protocols = stub.list_protocols(list_request)
print("Found protocols: %s" % available_protocols)
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# Set the sample id for the next protocol:
#
print("Setting sample id:")

# Construct a set sample id message to send to MinKNOW
set_sample_id_request = protocol.SetSampleIdRequest()
# Specify the sample id to set for the next protocol
set_sample_id_request.sample_id = "sample_id"

# Send the message to MinKNOW and wait for a response
stub.set_sample_id(set_sample_id_request)
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# Start one of the found protocols:
#

# Find a protocol to start from the available list
protocol_to_start = find_protocol(
    available_protocols,
    flow_cell="FLO-MIN106",
    kit="SQK-LSK108",
    experiment_type="sequencing")
print("Starting protocol: %s" % protocol_to_start.name)

# Construct a user info message to control the protocol group id
protocol_user_info = protocol.ProtocolRunUserInfo(
    # We need to specify StringValue as the group_id uses a nullable wrapper type
    protocol_group_id=StringValue(value="My Experiment Group")
)

# Construct a start protocol message to send to MinKNOW
start_request = protocol.StartProtocolRequest()

# Set the protocol identifier in the start message
# Start the first protocol in the returned list
start_request.identifier = protocol_to_start.identifier
start_request.user_info.CopyFrom(protocol_user_info)

# Send the start protocol and wait for the response
started_protocol = stub.start_protocol(start_request)
print("Started protocol run_id: %s" % started_protocol.run_id)
#-------------------------------------------------------------------------------
