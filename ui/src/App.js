import React, { useState } from 'react';
import './App.css'; // Don't forget to create a corresponding CSS file
import TableRow from './TableRow'; // Assuming TableRow is in the same directory

const App = () => {
  const staticContents = ['Static Content 1', 'Static Content 2', 'Static Content 3'];
  const [updatedRows, setUpdatedRows] = useState(staticContents);

  const handleUpdate = (index, newData) => {
    setUpdatedRows(prevRows => {
      const updated = [...prevRows];
      updated[index] = newData;
      return updated;
    });
  };

  return (
    <div className="app-container">
      <h1>Data Table</h1>
      <table>
        <thead>
          <tr>
            <th>Data</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {updatedRows.map((staticData, index) => (
            <TableRow key={index} index={index} staticData={staticData} onUpdate={handleUpdate} />
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default App;
