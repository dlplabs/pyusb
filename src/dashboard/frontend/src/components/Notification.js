
import React from 'react';
import PropTypes from 'prop-types';

function Notification({ message, type, onClose }) {
  return (
    <div className={`notification ${type}`}>
      {message}
      <button style={{ float: 'right' }} onClick={onClose}>×</button>
    </div>
  );
}

Notification.propTypes = {
  message: PropTypes.string.isRequired,
  type: PropTypes.string,
  onClose: PropTypes.func.isRequired
};

export default Notification;
