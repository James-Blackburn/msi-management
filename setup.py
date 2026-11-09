import os
import sys
import pwd
import subprocess
import pathlib

# Get actual user, even when running with sudo
username = os.environ.get("SUDO_USER", os.environ["USER"])
user = pwd.getpwnam(username)
home = pathlib.Path(user.pw_dir)

# Path to your application
app_path = pathlib.Path(__file__).resolve().parent / "src" / "main.py"
python_path = pathlib.Path(__file__).resolve().parent / "venv" / "bin" / "python"

# 1. Create autostart entry
autostart_dir = home / ".config" / "autostart"
autostart_dir.mkdir(parents=True, exist_ok=True)

desktop_file = autostart_dir / "msi-management.desktop"
desktop_file.write_text(f"""[Desktop Entry]
Type=Application
Name=MSI CPU & Fan Applet
Comment=Python background tray applet for MSI CPU and Fan management
Exec={python_path} {app_path}
Terminal=false
X-GNOME-Autostart-enabled=true
""")

os.chown(autostart_dir, user.pw_uid, user.pw_gid)
os.chown(desktop_file, user.pw_uid, user.pw_gid)

# 2. Add passwordless sudo permission for tee
sudoers_file = pathlib.Path("/etc/sudoers.d/msi-management")
device_attribute_list = [
    '/sys/devices/platform/msi-ec/cooler_boost',
    '/sys/devices/platform/msi-ec/fan_mode',
    '/sys/devices/platform/msi-ec/shift_mode'
]
permission_str = ''

for attribute in device_attribute_list:
    permission_str += f"{username} ALL=(root) NOPASSWD: " \
                      f"/usr/bin/tee {attribute}\n"

sudoers_file.write_text(permission_str)
sudoers_file.chmod(0o440)

# Validate sudoers configuration
subprocess.run(
    ["visudo", "-cf", str(sudoers_file)],
    check=True
)

print("Setup complete!")
