#-------------------------------------------------------------------------------
# This example will show you how to list available devices using minknow's
# manager api.
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
import minknow.rpc.manager_pb2 as manager
import minknow.rpc.manager_pb2_grpc as manager_grpc

# Import the grpc libraries we installed earlier
import grpc
#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
# Connect to the running Manager instance:
#
# We can connect to minknow manager on port 9501.
#
channel = grpc.insecure_channel('localhost:9501')
stub = manager_grpc.ManagerServiceStub(channel)
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# Send the list request
list_request = manager.ListDevicesRequest()
response = stub.list_devices(list_request)
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# We can now iterate and find our required device
for device in response.active:
    print("Found device %s using gRPC port %s" % (device.name, device.ports.insecure_grpc))