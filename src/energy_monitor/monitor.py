import logging
from datetime import datetime

class EnergyMonitor:
    def __init__(self):
        self.energy_log = {}

    def log_energy(self, device_id, energy_mWh):
        timestamp = datetime.utcnow().isoformat()
        if device_id not in self.energy_log:
            self.energy_log[device_id] = []
        self.energy_log[device_id].append({'timestamp': timestamp, 'energy_mWh': energy_mWh})
        logging.info(f"Logged {energy_mWh} mWh for device {device_id} at {timestamp}")

    def get_energy(self, device_id):
        return self.energy_log.get(device_id, [])

    def get_all_energy(self):
        return self.energy_log

    def update_from_usb(self, usb_manager):
        # Example: poll USBManager for energy data
        for dev in usb_manager._find_devices():
            energy = usb_manager.get_device_energy(dev.idProduct)
            self.log_energy(dev.idProduct, energy.get('energy_mWh', 0))
