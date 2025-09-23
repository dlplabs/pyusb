import { useState, useEffect, useCallback } from 'react';
import axios from 'axios';

const API_BASE = 'http://localhost:5001/api';

export function useDevices() {
  const [devices, setDevices] = useState([]);
  const [error, setError] = useState(null);

  const fetchDevices = useCallback(async () => {
    try {
      const res = await axios.get(`${API_BASE}/devices`);
      setDevices(res.data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch devices');
    }
  }, []);

  useEffect(() => {
    fetchDevices();
    const interval = setInterval(fetchDevices, 3000);
    return () => clearInterval(interval);
  }, [fetchDevices]);

  return { devices, fetchDevices, error };
}

export function useEnergy() {
  const [energy, setEnergy] = useState({});
  const [error, setError] = useState(null);

  const fetchEnergy = useCallback(async () => {
    try {
      await axios.post(`${API_BASE}/energy/update`);
      const res = await axios.get(`${API_BASE}/energy`);
      setEnergy(res.data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch energy data');
    }
  }, []);

  useEffect(() => {
    fetchEnergy();
    const interval = setInterval(fetchEnergy, 3000);
    return () => clearInterval(interval);
  }, [fetchEnergy]);

  return { energy, fetchEnergy, error };
}

export function useNotification() {
  const [notification, setNotification] = useState(null);
  const showNotification = (message, type = 'info') => {
    setNotification({ message, type });
  };
  const closeNotification = () => setNotification(null);
  return { notification, showNotification, closeNotification };
}
