# USB Control Dashboard

A Python 3 application to control and monitor USB ports, track energy usage, and visualize/manipulate port states via a web dashboard.

## Features
- USB port status and control (enable/disable)
- Real-time energy usage tracking per port
- Web dashboard with interactive charts, device filtering/search, modals, notifications
- RESTful API endpoints for all hardware/data access
- Advanced UI: auto-refresh, status indicators, modals, notifications, responsive layout, energy management controls
- Dockerized deployment for easy setup

## Requirements
- Python 3.8+
- `pyusb`
- `Flask`
- `pytest` (for testing)
- (Optional) `chart.js` for frontend charts
- Docker & Docker Compose (for containerized setup)

## Installation (Local)
1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd pyusb/src
   ```
2. Create and activate a virtual environment (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   If `requirements.txt` is missing, install manually:
   ```bash
   pip install pyusb flask pytest
   ```

## Installation & Startup (Native)
1. Install system dependencies:
   ```bash
   sudo apt-get update
   sudo apt-get install libusb-1.0-0
   ```
2. Create and activate a Python virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install Python dependencies:
   ```bash
   pip install pyusb flask pytest
   ```
4. Run the backend (API server) on port 5001 **with root permissions for USB access**:
   ```bash
   sudo venv/bin/python main.py
   # Or edit main.py to use: app.run(host='0.0.0.0', port=5001, debug=True)
   ```
5. Serve the frontend (static files) on port 5000:
   ```bash
   # From dashboard/static directory:
   python3 -m http.server 5000
   # Or use nginx for production
   ```
6. Access the dashboard in your browser:
   - Frontend: `http://localhost:5000`
   - Backend API: `http://localhost:5001`
   The frontend will communicate with the backend API on port 5001.

## Installation & Startup (Docker)
1. Build and start the backend and frontend applications using Docker Compose v2:
   ```bash
   sudo docker compose up --build
   ```
2. Access the dashboard in your browser:
   - Frontend: `http://localhost:5000`
   - Backend API: `http://localhost:5001`
   The React frontend (nginx) will communicate with the Flask backend API on port 5001.

> **Note:** If you encounter errors with `docker-compose`, upgrade to Docker Compose v2 and use `docker compose` (with a space).
> The backend (Flask API) and frontend (React/nginx) run as separate services and ports.

## Installation & Startup (Native Backend + Docker Frontend)
1. Start the backend (Flask API) natively (with root permissions and virtualenv):
   ```bash
   sudo venv/bin/python main.py
   # Backend API will run on http://localhost:5001
   ```
2. Build and start the frontend (React/nginx) using Docker Compose:
   ```bash
   sudo docker compose up --build
   # Frontend will run on http://localhost:5000
   ```
3. Access the dashboard in your browser:
   - Frontend: `http://localhost:5000`
   - Backend API: `http://localhost:5001`
   The React frontend will communicate with the Flask backend API on port 5001.

> **Note:** The backend must always be started natively (outside Docker). Only the frontend runs in Docker. If you encounter errors with `docker-compose`, upgrade to Docker Compose v2 and use `docker compose` (with a space).

## Usage
- View all USB ports and their status
- Enable/disable ports via dashboard
- Disabling a port via the dashboard will also block the device at the OS level (Linux) using a udev rule for persistent disablement. This is automated via the integrated `block_usb.sh` script.
- View and manage energy usage per port
- Use search/filter, charts, modals, and notifications for advanced interaction
- Energy management controls available per port (UI placeholder, extend as needed)

## Testing
Run all tests with:
```bash
pytest
```

## Troubleshooting
- To unblock a device, manually remove the corresponding line from `/etc/udev/rules.d/99-usb-block.rules` and reload udev:
   ```bash
   sudo nano /etc/udev/rules.d/99-usb-block.rules
   # Remove the line for your device
   sudo udevadm control --reload
   sudo udevadm trigger
   ```
- Ensure you have permissions to access USB devices (may require sudo/root on Linux)
- For Docker, run with `sudo` if you need USB device access
- Check logs for hardware/API errors
- For frontend issues, check browser console for errors
- If you see `externally-managed-environment` errors, use a Python virtual environment and run the backend with root permissions as shown above
- If using Docker Compose v2, ensure you are using the correct command syntax (`docker compose` instead of `docker-compose`)

## Project Structure
- `main.py` — Application entry point
- `usb_control/usb_manager.py` — USB hardware logic
- `energy_monitor/monitor.py` — Energy tracking
- `dashboard/app.py` — Web server/API
- `dashboard/templates/` — HTML templates
- `dashboard/static/` — JS/CSS/frontend assets
- `Dockerfile` — Container build file
- `docker-compose.yml` — Multi-container orchestration

---
For more details, see `.github/copilot-instructions.md` or ask for help.
