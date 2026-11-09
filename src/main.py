import os
import sys

os.environ["QT_QPA_PLATFORMTHEME"] = "generic"

from PySide6.QtWidgets import (
    QApplication,
    QSystemTrayIcon,
    QMenu,
    QStyle,
)
from PySide6.QtGui import QActionGroup
from msiec import MSIEC


class MSIManagementApplet:

    def __init__(self, app: QApplication):
        # System tray icon
        self.tray = QSystemTrayIcon()
        icon = app.style().standardIcon(
            QStyle.StandardPixmap.SP_ComputerIcon
        )
        self.tray.setIcon(icon)
        self.tray.setToolTip("Cooler Boost Applet")

        # Define Dropdown menu
        self.menu = QMenu()

        # Cooler Boost action
        self.boost_status = MSIEC.get_cooler_boost() == 'on'
        self.cooler_toggle = self.menu.addAction("Cooler Boost")
        self.cooler_toggle.setCheckable(True)
        self.cooler_toggle.setChecked(self.boost_status)
        self.cooler_toggle.toggled.connect(self.toggle_cooler_boost)
        self.menu.addSeparator()

        # Fan mode actions
        fan_modes = MSIEC.get_available_fan_modes()
        fan_group = QActionGroup(self.menu)
        fan_group.setExclusive(True)

        for mode in fan_modes:
            action = self.menu.addAction(mode)
            action.setCheckable(True)
            action.setData(mode)
            fan_group.addAction(action)

        fan_group.triggered.connect(
            lambda action: MSIEC.set_fan_mode(action.data())
        )
        fan_group.actions()[fan_modes.index(MSIEC.get_fan_mode())].setChecked(True)
        self.menu.addSeparator()

        # Shift mode actions
        shift_modes = MSIEC.get_available_shift_modes()
        shift_group = QActionGroup(self.menu)
        shift_group.setExclusive(True)

        for mode in shift_modes:
            action = self.menu.addAction(mode)
            action.setCheckable(True)
            action.setData(mode)
            shift_group.addAction(action)

        shift_group.triggered.connect(
            lambda action: MSIEC.set_shift_mode(action.data())
        )
        shift_group.actions()[shift_modes.index(MSIEC.get_shift_mode())].setChecked(True)
        self.menu.addSeparator()

        # Quit action
        self.quit = self.menu.addAction("Quit")
        self.quit.triggered.connect(app.quit)

        self.tray.setContextMenu(self.menu)
        self.tray.show()

    def toggle_cooler_boost(self) -> None:
        self.boost_status = not self.boost_status
        MSIEC.set_cooler_boost(self.boost_status)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    applet = MSIManagementApplet(app)
    sys.exit(app.exec())
