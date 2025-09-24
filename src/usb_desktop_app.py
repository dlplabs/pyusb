import os

import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QTableWidget, QTableWidgetItem,
    QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QHeaderView, QFrame
)
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import Qt
from usb_control.usb_manager import USBManager, IUSBManager
from energy_monitor.monitor import EnergyMonitor

class USBMonitorApp(QMainWindow):
    def __init__(self, usb_manager=None, energy_monitor=None):
        super().__init__()
        self.setWindowTitle('USB Energy Monitor')
        self.setGeometry(100, 100, 900, 600)

        # Set modern palette
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(245, 248, 255))
        palette.setColor(QPalette.Base, QColor(255, 255, 255))
        palette.setColor(QPalette.AlternateBase, QColor(230, 240, 255))
        palette.setColor(QPalette.Text, QColor(40, 40, 40))
        self.setPalette(palette)

        # Dependency injection for backend modules
        self.usb_manager = usb_manager if usb_manager else USBManager()
        self.energy_monitor = energy_monitor if energy_monitor else EnergyMonitor()

        # Main UI
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        main_layout = QVBoxLayout(self.central_widget)

        # Title
        title = QLabel('USB Energy Monitor Dashboard', self)
        title.setFont(QFont('Arial', 22, QFont.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        # Table frame
        table_frame = QFrame(self)
        table_frame.setFrameShape(QFrame.StyledPanel)
        table_layout = QVBoxLayout(table_frame)

        self.table = QTableWidget(self)
        self.table.setAlternatingRowColors(True)
        self.table.setColumnCount(7)  # Added column for control buttons
        self.table.setHorizontalHeaderLabels(['ID', 'Vendor', 'Product', 'Serial', 'Active', 'Energy (mWh)', 'Control'])
        self.table.setStyleSheet('QTableWidget { background: #fff; border: 1px solid #b0c4de; }'
                                 'QHeaderView::section { background-color: #e3eafc; font-weight: bold; }')
        header = self.table.horizontalHeader()
        if header is not None:
            header.setSectionResizeMode(QHeaderView.Stretch)
        table_layout.addWidget(self.table)

        main_layout.addWidget(table_frame)

        # Controls
        controls_layout = QHBoxLayout()
        self.refresh_button = QPushButton('Refresh', self)
        self.refresh_button.setStyleSheet('background-color: #4f8cff; color: white; font-weight: bold; padding: 6px 18px; border-radius: 6px;')
        self.refresh_button.clicked.connect(self.refresh_table)
        controls_layout.addWidget(self.refresh_button)

        main_layout.addLayout(controls_layout)

        self.refresh_table()

    def refresh_table(self):
        try:
            devices = self.usb_manager.get_ports_status()
            self.table.setRowCount(len(devices))
            self.table.setColumnCount(7)
            self.table.setHorizontalHeaderLabels(['ID', 'Vendor', 'Product', 'Serial', 'Active', 'Energy (mWh)', 'Control'])
            
            for row, dev in enumerate(devices):
                # Device info columns with error handling
                for col, key in enumerate(['id', 'vendor', 'product', 'serial', 'active']):
                    value = str(dev.get(key, 'N/A'))
                    item = QTableWidgetItem(value)
                    item.setFont(QFont('Arial', 11))
                    
                    # Highlight active status
                    if key == 'active':
                        if value.lower() == 'true':
                            item.setBackground(QColor('#E8F5E9'))  # Light green
                        elif value.lower() == 'false':
                            item.setBackground(QColor('#FFEBEE'))  # Light red
                    
                    self.table.setItem(row, col, item)
                
                # Energy column with error handling
                try:
                    energy = self.usb_manager.get_device_energy(dev.get('id', ''))
                    energy_value = energy.get('energy_mWh', 0)
                except Exception:
                    energy_value = 0
                
                energy_item = QTableWidgetItem(f"{energy_value:.2f}")
                energy_item.setFont(QFont('Arial', 11))
                self.table.setItem(row, 5, energy_item)
                
                # Control buttons with improved UI
                control_widget = QWidget()
                control_layout = QHBoxLayout(control_widget)
                control_layout.setContentsMargins(4, 4, 4, 4)
                control_layout.setSpacing(8)
                
                enable_btn = QPushButton('Enable')
                disable_btn = QPushButton('Disable')
                
                # Update button states based on device status
                is_active = str(dev.get('active', '')).lower() == 'true'
                enable_btn.setEnabled(not is_active)
                disable_btn.setEnabled(is_active)
                
                enable_btn.setStyleSheet('''
                    QPushButton {
                        background-color: #4CAF50;
                        color: white;
                        font-weight: bold;
                        padding: 4px 12px;
                        border-radius: 4px;
                    }
                    QPushButton:disabled {
                        background-color: #A5D6A7;
                    }
                    QPushButton:hover {
                        background-color: #43A047;
                    }
                ''')
                
                disable_btn.setStyleSheet('''
                    QPushButton {
                        background-color: #f44336;
                        color: white;
                        font-weight: bold;
                        padding: 4px 12px;
                        border-radius: 4px;
                    }
                    QPushButton:disabled {
                        background-color: #EF9A9A;
                    }
                    QPushButton:hover {
                        background-color: #E53935;
                    }
                ''')
                
                enable_btn.clicked.connect(lambda checked, d=dev: self.enable_device(d))
                disable_btn.clicked.connect(lambda checked, d=dev: self.disable_device(d))
                
                control_layout.addWidget(enable_btn)
                control_layout.addWidget(disable_btn)
                
                self.table.setCellWidget(row, 6, control_widget)
                
            # Optimize column sizes
            self.table.resizeColumnsToContents()
            
        except Exception as e:
            from PyQt5.QtWidgets import QMessageBox
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText(f"Error refreshing device list: {str(e)}")
            msg.setWindowTitle("Error")
            msg.exec_()
            
    def enable_device(self, device):
        success = self.usb_manager.set_port_state(device['id'], True, vendor_id=device['vendor'])
        if success:
            self.refresh_table()
            
    def disable_device(self, device):
        success = self.usb_manager.set_port_state(device['id'], False, vendor_id=device['vendor'])
        if success:
            self.refresh_table()

if __name__ == '__main__':
    # Check for root/admin privileges
    if os.geteuid() != 0:
        from PyQt5.QtWidgets import QMessageBox
        app = QApplication(sys.argv)
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("This application requires administrator privileges to access USB devices.\nPlease run with sudo.")
        msg.setWindowTitle("Admin Privileges Required")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
        sys.exit(1)
    app = QApplication(sys.argv)
    window = USBMonitorApp()
    window.show()
    sys.exit(app.exec_())
