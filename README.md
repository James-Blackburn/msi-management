# MSI Management Applet

System tray applet for easy management of MSI laptop CPU & Fan modes on Linux devices.
Requires MSI-EC driver (https://github.com/MControlSuite/msi-ec) to be installed on the system.
Does not poll CPU temps or Fan speeds to prevent system freezes.

# Usage

1. Create Python virtual environment (named venv) alongside the src directory.
2. Run setup.py as sudo user to enable user write access to msi-ec attributes & configure the application for autostart on boot.
3. Restart and interact with application via system tray.

# Tested Platforms

- MSI Thin GF63 12VE