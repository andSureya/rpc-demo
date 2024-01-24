from fastapi import FastAPI, WebSocket
import requests
import pendulum
import asyncio

from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from clock_pb2_grpc import ClockServiceStub
from clock_pb2 import TimestampMessage
import grpc


app = FastAPI()
# Mount the "static" directory to serve static files like CSS
app.mount("/static", StaticFiles(directory="templates/static"), name="static")

# Create an instance of the Jinja2Templates class
templates = Jinja2Templates(directory="templates")


html = """
<!DOCTYPE html>
<html>
<head>
    <title>FastAPI Table Example</title>
    <link rel="stylesheet" href="http://127.0.0.1:8000/static/styles.css">
</head>

<script src="http://127.0.0.1:8000/static/helpers.js"></script>

<body>
<h2>RPC demo</h2>
<table id="value-table">
    <tbody>
    <tr>
        <th>Time</th>
        <th>Action</th>
        <th>The 'Language'</th>
        <th>Action</th>
    </tr>
    <tr>
        <td>JSON time</td>
        <td>Data1</td>
        <td>JSON</td>
        <td>
            <button onclick="updateCell('button1')" id='button1'>Refresh</button>
        </td>
    </tr>
    <tr>
        <td>RPC time</td>
        <td>Data2</td>
        <td>RPC request</td>
        <td>
            <button onclick="updateCell('button2')" id='button2'>Refresh</button>
        </td>
    </tr>
    <tr>
        <td>Streamed time</td>
        <td>Data3</td>
        <td>RPC stream</td>
        <td>
            <button disabled="true" onclick="updateCell('button2')">Refresh</button>
        </td>
    </tr>
    </tbody>
</table>

<script>
    const socket = new WebSocket("ws://localhost:8000/ws");

    socket.onmessage = (event) => {
        const value = event.data;
        const table = document.getElementById("value-table");
        const cellToUpdate = table.rows[3].cells[1];
    };

</script>
</body>
</html>
"""


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        # Stream the updated value every second
        await websocket.send_text(pendulum.now().to_datetime_string())
        await asyncio.sleep(1)


@app.get("/action/{button_id}")
def parse(button_id: str):
    try:
        if button_id == "button1":
            url = "http://worldtimeapi.org/api/timezone/Europe/London"
            response = requests.get(url)
            data = response.json()
            result = pendulum.parser.parse(data['datetime']).to_datetime_string()
        else:
            stub = ClockServiceStub(grpc.insecure_channel('localhost:50051'))
            empty_request = TimestampMessage()
            rpc_result = stub.GetTimestamp(empty_request)
            result = rpc_result.timestamp

        return {
            'result': result
        }
    except Exception as e:
        print(e)


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


if __name__ == "__main__":
    import uvicorn

    # Run the FastAPI application using Uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=False)
