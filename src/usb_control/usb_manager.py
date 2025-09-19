import usb.core
import usb.util
import logging


class USBManager:
    def _find_devices(self):
        try:
            return list(usb.core.find(find_all=True))
        except Exception as e:
            logging.error(f"USB backend error: {e}")
            return []

    def get_ports_status(self):
        devices = self._find_devices()
        status = []
        for dev in devices:
            try:
                # Try to get serial, fallback to 'unknown' if not available
                serial = None
                if dev.iSerialNumber:
                    try:
                        serial = usb.util.get_string(dev, dev.iSerialNumber)
                    except Exception:
                        serial = 'unknown'
                # Try to get product, fallback to 'unknown' if not available
                product = getattr(dev, 'product', None)
                if product is None:
                    try:
                        product = usb.util.get_string(dev, dev.iProduct) if hasattr(dev, 'iProduct') and dev.iProduct else 'unknown'
                    except Exception:
                        product = 'unknown'
                status.append({
                    'id': dev.idProduct,
                    'vendor': dev.idVendor,
                    'product': product,
                    'serial': serial,
                    'active': dev.is_kernel_driver_active(0) if hasattr(dev, 'is_kernel_driver_active') else None
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
            match = dev.idProduct == device_id
            if vendor_id:
                match = match and (dev.idVendor == vendor_id)
            if serial:
                try:
                    match = match and (usb.util.get_string(dev, dev.iSerialNumber) == serial)
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
