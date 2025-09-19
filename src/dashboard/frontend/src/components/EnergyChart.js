import React from 'react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

function EnergyChart({ energy }) {
  const deviceIds = Object.keys(energy);
  const timestamps = deviceIds.length > 0 ? energy[deviceIds[0]].map(log => log.timestamp) : [];
  const datasets = deviceIds.map(deviceId => ({
    label: `Device ${deviceId}`,
    data: energy[deviceId].map(log => log.energy_mWh),
    borderColor: '#' + Math.floor(Math.random()*16777215).toString(16),
    fill: false
  }));

  const data = {
    labels: timestamps,
    datasets
  };

  const options = {
    responsive: true,
    plugins: {
      legend: { display: true },
      title: { display: true, text: 'Energy Usage (mWh)' }
    }
  };

  return (
    <div>
      <h2>Energy Usage</h2>
      <Line data={data} options={options} />
    </div>
  );
}

export default EnergyChart;
