import React, { useEffect, useState } from 'react';
import axios from 'axios';
import DeviceTable from './components/DeviceTable';
import EnergyChart from './components/EnergyChart';
import Notification from './components/Notification';
import './App.css';

const API_BASE = 'http://localhost:5001/api';

function App() {
  const [devices, setDevices] = useState([]);
  const [energy, setEnergy] = useState({});
  const [notification, setNotification] = useState(null);

  useEffect(() => {
    fetchDevices();
    fetchEnergy();
    const interval = setInterval(() => {
      fetchDevices();
      fetchEnergy();
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  const fetchDevices = async () => {
    try {
      const res = await axios.get(`${API_BASE}/devices`);
      setDevices(res.data);
    } catch (err) {
      setNotification({ message: 'Failed to fetch devices', type: 'error' });
    }
  };

  const fetchEnergy = async () => {
    try {
      await axios.post(`${API_BASE}/energy/update`);
      const res = await axios.get(`${API_BASE}/energy`);
      setEnergy(res.data);
    } catch (err) {
      setNotification({ message: 'Failed to fetch energy data', type: 'error' });
    }
  };

  const manageDevice = async (deviceId, action) => {
    try {
      const res = await axios.post(`${API_BASE}/devices/${deviceId}/manage`, { action });
      if (res.data.success) {
        setNotification({ message: 'Device state updated.', type: 'info' });
        fetchDevices();
      } else {
        setNotification({ message: 'Failed to update device.', type: 'error' });
      }
    } catch (err) {
      setNotification({ message: 'Error updating device.', type: 'error' });
    }
  };

  return (
    <div className="container">
      <h1>USB Control Dashboard</h1>
      <DeviceTable devices={devices} onManage={manageDevice} />
      <EnergyChart energy={energy} />
      {notification && <Notification {...notification} onClose={() => setNotification(null)} />}
    </div>
  );
}

export default App;
