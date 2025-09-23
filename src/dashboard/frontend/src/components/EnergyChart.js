
import React from 'react';
import PropTypes from 'prop-types';
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

const COLORS = [
  '#4f8cff', '#ff4f4f', '#4fff8c', '#ffb84f', '#8c4fff', '#4fffd6', '#ffd64f', '#4f8cff'
];

function EnergyChart({ energy }) {
  const deviceIds = Object.keys(energy);
  const timestamps = deviceIds.length > 0 ? energy[deviceIds[0]].map(log => log.timestamp) : [];
  const datasets = deviceIds.map((deviceId, idx) => ({
    label: `Device ${deviceId}`,
    data: energy[deviceId].map(log => log.energy_mWh),
    borderColor: COLORS[idx % COLORS.length],
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

EnergyChart.propTypes = {
  energy: PropTypes.object.isRequired
};

export default EnergyChart;
