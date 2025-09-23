
import React from 'react';
import PropTypes from 'prop-types';

function DeviceActionButtons({ deviceId, onManage }) {
  return (
    <>
      <button onClick={() => onManage(deviceId, 'enable')}>Enable</button>
      <button onClick={() => onManage(deviceId, 'disable')}>Disable</button>
    </>
  );
}

DeviceActionButtons.propTypes = {
  deviceId: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
  onManage: PropTypes.func.isRequired
};

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
                <DeviceActionButtons deviceId={device.id} onManage={onManage} />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

DeviceTable.propTypes = {
  devices: PropTypes.arrayOf(PropTypes.object).isRequired,
  onManage: PropTypes.func.isRequired
};

export default DeviceTable;
