import React from 'react';

function DeviceTable({ devices, onManage }) {
  return (
    <div>
      <h2>Ports Status</h2>
      <table className="device-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Vendor</th>
            <th>Product</th>
            <th>Serial</th>
            <th>Status</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {devices.map(device => (
            <tr key={device.id + '-' + device.vendor}>
              <td>{device.id}</td>
              <td>{device.vendor}</td>
              <td>{device.product || ''}</td>
              <td>{device.serial || ''}</td>
              <td>
                <span className={device.active ? 'status-indicator status-active' : 'status-indicator status-inactive'}></span>
                {device.active ? 'Active' : 'Inactive'}
              </td>
              <td>
                <button onClick={() => onManage(device.id, 'enable')}>Enable</button>
                <button onClick={() => onManage(device.id, 'disable')}>Disable</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default DeviceTable;
