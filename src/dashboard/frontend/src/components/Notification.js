import React from 'react';

function Notification({ message, type, onClose }) {
  return (
    <div className={`notification ${type}`}>
      {message}
      <button style={{ float: 'right' }} onClick={onClose}>×</button>
    </div>
  );
}

export default Notification;
