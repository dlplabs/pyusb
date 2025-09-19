from flask import Flask, jsonify, request
from usb_control.usb_manager import USBManager
from energy_monitor.monitor import EnergyMonitor
import logging

from flask import render_template
import os

app = Flask(__name__, static_folder='static', template_folder='templates')
usb_manager = USBManager()
energy_monitor = EnergyMonitor()

@app.route('/api/ports', methods=['GET'])
def get_ports():
    return jsonify(usb_manager.get_ports_status())

@app.route('/api/ports/<int:device_id>/state', methods=['POST'])
def set_port_state(device_id):
    data = request.get_json()
    enable = data.get('enable', True)
    result = usb_manager.set_port_state(device_id, enable)
    return jsonify({'success': result})

@app.route('/api/energy', methods=['GET'])
def get_all_energy():
    return jsonify(energy_monitor.get_all_energy())

@app.route('/api/energy/<int:device_id>', methods=['GET'])
def get_device_energy(device_id):
    return jsonify(energy_monitor.get_energy(device_id))

@app.route('/api/energy/update', methods=['POST'])
def update_energy():
    energy_monitor.update_from_usb(usb_manager)
    return jsonify({'success': True})

@app.errorhandler(Exception)
def handle_exception(e):
    logging.error(f"API error: {e}")
    return jsonify({'error': str(e)}), 500

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

# List connected USB devices
@app.route('/api/devices', methods=['GET'])
def list_devices():
    return jsonify(usb_manager.get_ports_status())

# Manage (enable/disable) a device
@app.route('/api/devices/<int:device_id>/manage', methods=['POST'])
def manage_device(device_id):
    import subprocess
    data = request.get_json()
    action = data.get('action')
    vendor_id = data.get('vendor')
    # Try to get vendor_id if not provided
    if not vendor_id:
        # Find device in status list
        for dev in usb_manager.get_ports_status():
            if dev['id'] == device_id:
                vendor_id = dev['vendor']
                break
    if action == 'enable':
        result = usb_manager.set_port_state(device_id, True)
    elif action == 'disable':
        result = usb_manager.set_port_state(device_id, False)
        # Also block at OS level using block_usb.sh
        if vendor_id:
            try:
                subprocess.run([
                    os.path.abspath(os.path.join(os.path.dirname(__file__), '../block_usb.sh')),
                    str(vendor_id), str(device_id)
                ], check=True)
                logging.info(f"Device {vendor_id}:{device_id} blocked at OS level.")
            except Exception as e:
                logging.error(f"Failed to block device at OS level: {e}")
    else:
        return jsonify({'error': 'Invalid action'}), 400
    return jsonify({'success': result})

# Frontend route
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
