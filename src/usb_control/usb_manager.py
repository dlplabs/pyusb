
# Interface for USB device operations
class IUSBManager:
    def get_ports_status(self):
        raise NotImplementedError
    def set_port_state(self, device_id, enable, vendor_id=None, serial=None):
        raise NotImplementedError
    def get_device_energy(self, device_id):
        raise NotImplementedError

# Concrete implementation using pyusb
import usb.core
import usb.util
import logging

class USBManager(IUSBManager):
    def _find_devices(self):
        try:
            found = usb.core.find(find_all=True)
            if found is None:
                return []
            # Only include usb.core.Device instances
            from usb.core import Device
            return [dev for dev in found if isinstance(dev, Device)]
        except Exception as e:
            logging.error(f"USB backend error: {e}")
            return []

    def get_ports_status(self):
        devices = self._find_devices()
        status = []
        for dev in devices:
            try:
                serial = 'unknown'
                iSerial = getattr(dev, 'iSerialNumber', None)
                if iSerial:
                    try:
                        serial = usb.util.get_string(dev, iSerial)
                    except Exception:
                        pass
                product = 'unknown'
                iProduct = getattr(dev, 'iProduct', None)
                if iProduct:
                    try:
                        product = usb.util.get_string(dev, iProduct)
                    except Exception:
                        pass
                status.append({
                    'id': getattr(dev, 'idProduct', 'unknown'),
                    'vendor': getattr(dev, 'idVendor', 'unknown'),
                    'product': product,
                    'serial': serial,
                    'active': getattr(dev, 'is_kernel_driver_active', lambda x: None)(0)
                })
            except Exception as e:
                logging.error(f"Error reading device info: {e}")
                status.append({
                    'id': getattr(dev, 'idProduct', 'unknown'),
                    'vendor': getattr(dev, 'idVendor', 'unknown'),
                    'product': 'unknown',
                    'serial': 'unknown',
                    'active': None
                })
        return status

    def set_port_state(self, device_id, enable, vendor_id=None, serial=None):
        devices = self._find_devices()
        for dev in devices:
            match = getattr(dev, 'idProduct', None) == device_id
            if vendor_id:
                match = match and (getattr(dev, 'idVendor', None) == vendor_id)
            if serial:
                try:
                    match = match and (usb.util.get_string(dev, getattr(dev, 'iSerialNumber', None)) == serial)
                except Exception:
                    match = False
            if match:
                try:
                    if hasattr(dev, 'is_kernel_driver_active'):
                        if enable:
                            if not dev.is_kernel_driver_active(0):
                                dev.attach_kernel_driver(0)
                        else:
                            if dev.is_kernel_driver_active(0):
                                dev.detach_kernel_driver(0)
                        logging.info(f"Set device {device_id} state to {'enabled' if enable else 'disabled'}.")
                        return True
                    else:
                        logging.warning("Device does not support kernel driver operations.")
                        return False
                except Exception as e:
                    logging.error(f"Error setting port state: {e}")
                    return False
        logging.warning(f"Device {device_id} not found.")
        return False

    def get_device_energy(self, device_id):
        # Placeholder: Real energy data requires hardware support
        return {'device_id': device_id, 'energy_mWh': 0}
