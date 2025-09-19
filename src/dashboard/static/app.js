let portsCache = [];
let energyCache = {};
let autoRefreshInterval;

async function fetchDevices() {
    const res = await fetch('/api/devices');
    const devices = await res.json();
    renderDevices(devices);
}

function renderDevices(devices) {
    const tbody = document.querySelector('#ports-table tbody');
    tbody.innerHTML = '';
    devices.forEach(device => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${device.id}</td>
            <td>${device.vendor}</td>
            <td>${device.product || ''}</td>
            <td>${device.serial || ''}</td>
            <td><span class="status-indicator ${device.active ? 'status-active' : 'status-inactive'}"></span>${device.active ? 'Active' : 'Inactive'}</td>
            <td>
                <button onclick="manageDevice(${device.id}, 'enable')">Enable</button>
                <button onclick="manageDevice(${device.id}, 'disable')">Disable</button>
                <button onclick="showDeviceModal(${device.id})">Details</button>
                <button onclick="manageEnergy(${device.id})">Manage Energy</button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

async function manageDevice(deviceId, action) {
    const res = await fetch(`/api/devices/${deviceId}/manage`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action })
    });
    const result = await res.json();
    showNotification(result.success ? 'Device state updated.' : 'Failed to update device.', result.success ? 'info' : 'error');
    fetchDevices();
}

function filterPorts() {
    const query = document.getElementById('search').value.toLowerCase();
    const filtered = portsCache.filter(port =>
        String(port.id).includes(query) ||
        String(port.vendor).toLowerCase().includes(query) ||
        (port.product || '').toLowerCase().includes(query) ||
        (port.serial || '').toLowerCase().includes(query)
    );
    renderDevices(filtered);
}

async function fetchEnergy() {
    await fetch('/api/energy/update', { method: 'POST' });
    const res = await fetch('/api/energy');
    energyCache = await res.json();
    renderEnergy(energyCache);
    renderEnergyChart(energyCache);
}

function renderEnergy(energy) {
    const tbody = document.querySelector('#energy-table tbody');
    tbody.innerHTML = '';
    Object.entries(energy).forEach(([deviceId, logs]) => {
        logs.forEach(log => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${deviceId}</td>
                <td>${log.timestamp}</td>
                <td>${log.energy_mWh}</td>
            `;
            tbody.appendChild(tr);
        });
    });
}

function renderEnergyChart(energy) {
    if (typeof Chart === 'undefined') return;
    const ctx = document.getElementById('energy-chart').getContext('2d');
    const labels = [];
    const datasets = [];
    Object.entries(energy).forEach(([deviceId, logs]) => {
        labels.push(deviceId);
        datasets.push({
            label: `Device ${deviceId}`,
            data: logs.map(l => l.energy_mWh),
            fill: false,
            borderColor: '#' + Math.floor(Math.random()*16777215).toString(16),
        });
    });
    if (window.energyChart) window.energyChart.destroy();
    window.energyChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: Object.values(energy).flatMap(logs => logs.map(l => l.timestamp)),
            datasets: datasets
        },
        options: { responsive: true, plugins: { legend: { display: true } } }
    });
}

function showDeviceModal(deviceId) {
    const modal = document.getElementById('device-modal');
    const body = document.getElementById('modal-body');
    const port = portsCache.find(p => p.id === deviceId);
    body.innerHTML = `<h3>Device ${deviceId}</h3><pre>${JSON.stringify(port, null, 2)}</pre>`;
    modal.style.display = 'flex';
}

document.getElementById('close-modal').onclick = function() {
    document.getElementById('device-modal').style.display = 'none';
};
window.onclick = function(event) {
    const modal = document.getElementById('device-modal');
    if (event.target === modal) modal.style.display = 'none';
};

function showNotification(message, type = 'info') {
    if (typeof window.showNotification === 'function') {
        window.showNotification(message, type);
    }
}

function manageEnergy(deviceId) {
    showNotification('Energy management for device ' + deviceId + ' not yet implemented.', 'info');
    // Here you can add UI/modal for energy management controls
}

function startAutoRefresh() {
    if (autoRefreshInterval) clearInterval(autoRefreshInterval);
    autoRefreshInterval = setInterval(() => {
        fetchDevices();
        fetchEnergy();
    }, 3000);
}

function refresh() {
    fetchDevices();
    fetchEnergy();
    startAutoRefresh();
}

window.onload = refresh;
