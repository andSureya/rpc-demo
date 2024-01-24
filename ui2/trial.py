from time import sleep

import grpc
from clock_pb2_grpc import ClockServiceStub
from clock_pb2 import TimestampMessage  # Make sure to import your actual generated module

# Create a stub for the gRPC service
stub = ClockServiceStub(grpc.insecure_channel('localhost:50051'))

# Create an empty request for the GetTimestamp method
empty_request = TimestampMessage()

# Make the gRPC call to get data for "RPC time"
rpc_time_result = stub.GetTimestamp(empty_request)

# Now you can use the rpc_time_result as needed
print(rpc_time_result.timestamp)


# stream = stub.StreamTimestamp(empty_request)
# for response in stream:
#     print(response)
#     sleep(1)


