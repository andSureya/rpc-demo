
const socket = new WebSocket("ws://localhost:8000/ws");

    socket.onmessage = (event) => {
        const value = event.data;
        const table = document.getElementById("value-table");
        const cellToUpdate = table.rows[3].cells[1];
        cellToUpdate.innerHTML = value;
    };