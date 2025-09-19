# Copilot Instructions for USB Control Project

## Project Overview
This Python 3 project enables control and monitoring of USB ports, including status checks and energy usage tracking. It features a web-based dashboard for visualization and manipulation of port states. The codebase is organized for clear separation between hardware interaction and UI logic.

## Architecture & Key Components
- `usb_control/`: USB port communication and state manipulation. All hardware access via `pyusb`.
- `energy_monitor/`: Tracks/logs energy usage per port. Integrates with USB control for real-time data.
- `dashboard/`: Web UI (Flask recommended) for visualizing port status, energy data, and sending control commands. All UI logic interacts with hardware via API endpoints only.
- `main.py`: Entry point; wires together hardware modules and dashboard.

## Required Packages
- `pyusb` (USB hardware access)
- `Flask` (dashboard/API)
- `pytest` (testing)
- `logging` (debugging)

## Developer Workflows
- **Build/Run:**
  - Install dependencies: `pip install -r requirements.txt`
  - Start dashboard: `python main.py`
- **Testing:**
  - Tests in `tests/` (pytest convention)
  - Run: `pytest`
- **Debugging:**
  - Use Python `logging` in all modules. Log hardware errors and API exceptions; surface critical errors in dashboard UI and logs.
  - For hardware debugging, add verbose logging in `usb_control/` and expose error status via API.

## Project-Specific Conventions
- All hardware access is abstracted in `usb_control/`.
- Energy data is stored in `energy_monitor/` and exposed via API endpoints.
- UI logic does not directly access hardware; uses API calls only.
- All new features should include a dashboard control and visualization if relevant.
- API endpoints should follow RESTful conventions (e.g., `/api/ports`, `/api/energy`).
- Dashboard controls should manipulate port states via API, not direct hardware calls.
- Use clear, descriptive names for API routes and dashboard controls.

## Integration Points
- Relies on `pyusb` for USB communication
- Web dashboard uses Flask (see `dashboard/`)
- Data flows: USB state/energy → API → Dashboard

## Example Patterns
- To add a new USB feature:
  1. Extend `usb_control/usb_manager.py` with new hardware logic.
  2. Add/modify API endpoint in `dashboard/app.py` to expose the feature.
  3. Update dashboard UI to visualize/control the new feature via API.
- For new energy metrics:
  1. Update `energy_monitor/monitor.py` to track new metrics.
  2. Expose metrics via API in `dashboard/app.py`.
  3. Add dashboard visualization for new metrics.
- For debugging hardware/API issues:
  - Add detailed logging in relevant modules and ensure errors are visible in dashboard.

## Key Files
- `usb_control/usb_manager.py`: Main USB logic
- `energy_monitor/monitor.py`: Energy tracking
- `dashboard/app.py`: Web server
- `main.py`: Startup and integration

---
Follow these conventions for all new code. For questions, check `README.md` or ask for clarification.