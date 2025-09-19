import logging
from usb_control.usb_manager import USBManager
from energy_monitor.monitor import EnergyMonitor
import dashboard.app

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    usb_manager = USBManager()
    energy_monitor = EnergyMonitor()
    # Optionally, start periodic energy updates here
    logging.info("Starting USB Control Dashboard API on port 5001...")
    dashboard.app.app.run(host='0.0.0.0', port=5001, debug=True)
