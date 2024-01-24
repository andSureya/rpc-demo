import asyncio
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import grpc
import time

from starlette.responses import HTMLResponse

import clock_pb2_grpc
from backend.clock_pb2 import TimestampMessage

app = FastAPI()

# Mount the "static" directory to serve static files like CSS
app.mount("/static", StaticFiles(directory="templates/static"), name="static")

# Create an instance of the Jinja2Templates class
templates = Jinja2Templates(directory="templates")

stub = clock_pb2_grpc.ClockServiceStub(grpc.insecure_channel('localhost:50051'))


def stream_timestamp_data():
    try:
        request = TimestampMessage()  # Replace with the actual message type
        stream = stub.StreamTimestamp(request)
        for response in stream:
            yield response.timestamp  # Replace with the actual attribute in your response
    except grpc.aio.AioRpcError as e:
        print(f"Error during gRPC streaming: {e}")


def generate_updates(request: Request):
    table_data = [
        {"header1": "Time", "header2": "Action", "header3": "The 'Language'"},
        {"header1": "JSON time", "header2": "Row 1 Data 2", "header3": "JSON"},
        {"header1": "RPC time", "header2": "Row 2 Data 2", "header3": "RPC request"},
        {"header1": "Streamed time", "header2": "Row 3 Data 2", "header3": "RPC stream"},
    ]

    def get_streaming_data(request: Request):
        for timestamp in stream_timestamp_data():
            table_data.pop()
            table_data.append(
                {
                    "header1": "Streamed time",
                    "header2": timestamp,
                    "header3": "RPC stream",
                }
            )
            html_content = templates.TemplateResponse("index.html", {"table_data": table_data, "request": request}).body
            yield HTMLResponse(html_content)
            time.sleep(1)
            # await asyncio.sleep(0)

    return StreamingResponse(get_streaming_data(request))


@app.get("/")
async def read_root(request: Request):
    return generate_updates(request)

if __name__ == "__main__":
    import uvicorn

    # Run the FastAPI application using Uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=False)
