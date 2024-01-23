import React, { useState } from 'react';
import './App.css'; // Don't forget to create a corresponding CSS file

const TableRow = ({ index, staticData, onUpdate }) => {
  const [data, setData] = useState(staticData);
  const [loading, setLoading] = useState(false);
  const [lastRefreshed, setLastRefreshed] = useState('');

  const handleRefresh = async () => {
    setLoading(true);
    try {
      const newData = await fetchData(); // Replace with your actual fetching logic
      setData(newData);
      setLastRefreshed(new Date().toLocaleTimeString());
      onUpdate(index, newData);
    } finally {
      setLoading(false);
    }
  };

  // Simulate fetching data
  const fetchData = () => {
    return new Promise(resolve => {
      setTimeout(() => {
        // Simulating an API call
        resolve(`Refreshed Data ${index}`);
      }, 1000);
    });
  };

  return (
    <tr>
      <td>
        {loading ? (
          <div>
            Loading...
          </div>
        ) : (
          <div>
            {data}
            {lastRefreshed && <div>Last Refreshed at: {lastRefreshed}</div>}
          </div>
        )}
      </td>
      <td>
        <button onClick={handleRefresh} disabled={loading}>
          Refresh
        </button>
      </td>
    </tr>
  );
};

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
