async function updateCell(buttonId) {
    const response = await fetch('/action/'+buttonId);
    const resultData = await response.json();
    const updatedValue = resultData.result;
    const table = document.getElementById("value-table");
    let numericId;

    if (buttonId === "button1") {
        numericId = 1;
    } else {
        numericId = 2;
    }
    const cellToUpdate = table.rows[numericId].cells[1];
    cellToUpdate.innerHTML = updatedValue;
}
