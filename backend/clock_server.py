import grpc
from concurrent import futures
import time
from datetime import datetime

from google.protobuf import timestamp_pb2
from clock_pb2 import TimestampMessage
from clock_pb2_grpc import ClockServiceServicer, add_ClockServiceServicer_to_server


class ClockServer(ClockServiceServicer):
    def GetTimestamp(self, request, context):
        timestamp = timestamp_pb2.Timestamp()
        timestamp.GetCurrentTime()
        formatted_timestamp = self.format_timestamp(timestamp)
        return TimestampMessage(timestamp=formatted_timestamp)

    def StreamTimestamp(self, request, context):
        while context.is_active():
            time.sleep(1)
            timestamp = timestamp_pb2.Timestamp()
            timestamp.GetCurrentTime()
            formatted_timestamp = self.format_timestamp(timestamp)
            yield TimestampMessage(timestamp=formatted_timestamp)

    @staticmethod
    def format_timestamp(timestamp):
        # Convert timestamp to a formatted string
        dt = datetime.utcfromtimestamp(timestamp.ToSeconds())
        formatted_timestamp = dt.strftime("%Y-%m-%d %H:%M:%S")
        return formatted_timestamp


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_ClockServiceServicer_to_server(ClockServer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print('Server running at http://[::]:50051')
    try:
        while True:
            time.sleep(86400)  # One day in seconds
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
