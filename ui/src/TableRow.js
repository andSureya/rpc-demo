import React, { useState, useEffect } from 'react';
import { ClockServiceClient } from './ClockGRPCPb';

import { grpc } from 'grpc-web-client';

const TableRow = ({ index, staticData, onUpdate }) => {
  const [data, setData] = useState(staticData);
  const [loading, setLoading] = useState(false);
  const [lastRefreshed, setLastRefreshed] = useState('');

  useEffect(() => {
    // Use different methods for different rows
    if (index === 0) {
      // Row 1: Call GetTimestamp method
      handleGetTimestamp();
    } else if (index === 1) {
      // Row 2: Call StreamTimestamp method
      // handleStreamTimestamp();
    } else if (index === 2) {
      // Row 3: Call an API every 3 seconds
      const apiInterval = setInterval(() => {
        handleApiCall();
      }, 30009);

      // Cleanup the interval when the component unmounts
      return () => clearInterval(apiInterval);
    }
  }, [index]); // Run this effect whenever the index changes

  const handleGetTimestamp = async () => {
  setLoading(true);
  try {

    const client = new ClockServiceClient('http://localhost:50051', null, null);

    var messages = require('./ClockPb');

    const response = await grpc.unary(ClockServiceClient.GetTimestamp, {
      request: new messages.TimestampMessage(),
      host: 'http://localhost:50051',
    });


    const timestamp = response.message.toObject().timestamp;
    setData(timestamp);
    setLastRefreshed(new Date().toLocaleTimeString());
    onUpdate(index, timestamp);
  } catch (error) {
    console.error('Error calling GetTimestamp:', error);
  } finally {
    setLoading(false);
  }
};

//   const handleStreamTimestamp = () => {
//   // Initialize the streaming call
//     var messages = require('./ClockPb');
//   const stream = grpc.invoke(ClockServiceClient.StreamTimestamp, {
//     request: new messages.TimestampMessage(),
//     onMessage: (response) => {
//       const timestamp = response.toObject().timestamp;
//       setData(timestamp);
//       setLastRefreshed(new Date().toLocaleTimeString());
//     },
//     onEnd: (code, message, trailers) => {
//       // Handle stream closure
//       if (code === grpc.Code.OK) {
//         console.log('Stream completed successfully');
//       } else {
//         console.error(`Stream closed with error: ${code}, message: ${message}`);
//       }
//     },
//   });
//
//   // Cleanup the streaming call when the component unmounts
//   return () => {
//     // Close the streaming call (if not already closed)
//     if (stream) {
//       stream.close();
//     }
//   };
// };

  const handleApiCall = async () => {
    setLoading(true);
    try {
      // Replace the dummy API URL with your actual API endpoint
      const response = await fetch('http://worldtimeapi.org/api/timezone/Europe/London');
      const newData = await response.json();
      setData(newData['datetime']);
      setLastRefreshed(new Date().toLocaleTimeString());
      onUpdate(index, newData);
    } catch (error) {
      console.error('Error calling API:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleRefresh = async () => {
    setLoading(true);
    try {
      if (index === 0) {
        // For row 1, refresh using GetTimestamp method
        await handleGetTimestamp();
      } else if (index === 1) {
        // For row 2, refresh using StreamTimestamp method
        await handleStreamTimestamp();
      } else if (index === 2) {
        // For row 3, refresh using the API call
        await handleApiCall();
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <tr>
      <td>
        {loading ? (
          <div>Loading...</div>
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

export default TableRow;
