import asyncio
from concurrent.futures import ThreadPoolExecutor

from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import grpc
import time

import clock_pb2_grpc
from backend.clock_pb2 import TimestampMessage

app = FastAPI()

# Mount the "static" directory to serve static files like CSS
app.mount("/static", StaticFiles(directory="templates/static"), name="static")

# Create an instance of the Jinja2Templates class
templates = Jinja2Templates(directory="templates")

stub = clock_pb2_grpc.ClockServiceStub(grpc.insecure_channel('localhost:50051'))

executor = ThreadPoolExecutor()


def stream_timestamp_data() -> str:
    empty_request = TimestampMessage()
    stream = stub.StreamTimestamp(empty_request)
    for response in stream:
        val = response.timestamp
        yield val
        time.sleep(1)


def update_table(table_data, request):
    print("updating the table")
    for streaming_data in stream_timestamp_data():
        table_data.pop()
        table_data.append(
            {
                "header1": "Streamed time",
                "header2": streaming_data,
                "header3": "RPC stream",
            }
        )

        templates.TemplateResponse(
            "index.html", {"request": request, "table_data": table_data}
        )
        # await asyncio.sleep(0)  # Allow other tasks to run


@app.get("/")
async def read_root(request: Request):
    # Dummy data for the table
    empty_request = TimestampMessage()

    # gRPC Unary RPC call
    rpc_time_result = stub.GetTimestamp(empty_request)

    # Extract timestamp from the response
    rpc_time_str = rpc_time_result.timestamp  # Replace with the actual attribute in your response

    table_data = [
        {"header1": "Time", "header2": "Action", "header3": "The 'Language'"},
        {"header1": "JSON time", "header2": "Row 1 Data 2", "header3": "JSON"},
        {"header1": "RPC time", "header2": rpc_time_str, "header3": "RPC request"},
        {"header1": "Streamed time", "header2": "Row 3 Data 2", "header3": "RPC stream"},
    ]

    async def generate_updates():
        async for streaming_data in stream_timestamp_data():
            table_data.pop()
            table_data.append(
                {
                    "header1": "Streamed time",
                    "header2": streaming_data,
                    "header3": "RPC stream",
                }
            )
            yield templates.TemplateResponse("index.html", {"request": request, "table_data": table_data})
            await asyncio.sleep(0)  # Allow other tasks to run

    return generate_updates()  # No need for aiter here

if __name__ == "__main__":
    import uvicorn

    # Run the FastAPI application using Uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=False)
