
import React from 'react';
import DeviceTable from './components/DeviceTable';
import EnergyChart from './components/EnergyChart';
import Notification from './components/Notification';
import { useDevices, useEnergy, useNotification } from './hooks';
import axios from 'axios';
import './App.css';

function App() {
  const { devices, fetchDevices, error: deviceError } = useDevices();
  const { energy, fetchEnergy, error: energyError } = useEnergy();
  const { notification, showNotification, closeNotification } = useNotification();

  const manageDevice = async (deviceId, action) => {
    try {
      const res = await axios.post(`http://localhost:5001/api/devices/${deviceId}/manage`, { action });
      if (res.data.success) {
        showNotification('Device state updated.', 'info');
        fetchDevices();
      } else {
        showNotification('Failed to update device.', 'error');
      }
    } catch (err) {
      showNotification('Error updating device.', 'error');
    }
  };

  return (
    <div className="container">
      <h1>USB Control Dashboard</h1>
      <DeviceTable devices={devices} onManage={manageDevice} />
      <EnergyChart energy={energy} />
      {(notification || deviceError || energyError) && (
        <Notification
          message={notification?.message || deviceError || energyError}
          type={notification?.type || 'error'}
          onClose={closeNotification}
        />
      )}
    </div>
  );
}

export default App;
