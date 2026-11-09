from typing import List
import subprocess
import pathlib


class MSIEC:

    _EC_PATH = pathlib.Path('/sys/devices/platform/msi-ec')
    _COOLER_BOOST = 'cooler_boost'
    _AVAILABLE_FAN_MODES = 'available_fan_modes'
    _AVAILABLE_SHIFT_MODES = 'available_shift_modes'
    _FAN_MODE = 'fan_mode'
    _SHIFT_MODE = 'shift_mode'

    # Private methods

    @classmethod
    def _read(cls, attribute: str) -> str:
        return (cls._EC_PATH / attribute).read_text().strip()

    @classmethod
    def _write(cls, attribute: str, value: str) -> None:
        try:
            subprocess.run(
                ["sudo", "-n", "/usr/bin/tee", cls._EC_PATH / attribute],
                input=value + '\n',
                text=True,
                check=True
            )
        except subprocess.CalledProcessError as exc:
            print(f'Command failed with exit code {exc.returncode}')

    # Getters

    @classmethod
    def get_cooler_boost(cls) -> str:
        return cls._read(cls._COOLER_BOOST)

    @classmethod
    def get_fan_mode(cls) -> str:
        return cls._read(cls._FAN_MODE)

    @classmethod
    def get_available_fan_modes(cls) -> List[str]:
        fan_mode_list = cls._read(cls._AVAILABLE_FAN_MODES).split('\n')
        # Advanced fan mode is unsupported
        if 'advanced' in fan_mode_list:
            fan_mode_list.remove('advanced')
        return fan_mode_list

    @classmethod
    def get_available_shift_modes(cls) -> List[str]:
        return cls._read(cls._AVAILABLE_SHIFT_MODES).split('\n')

    @classmethod
    def get_shift_mode(cls) -> str:
        return cls._read(cls._SHIFT_MODE)

    # Setters

    @classmethod
    def set_cooler_boost(cls, enabled: bool) -> None:
        cls._write(cls._COOLER_BOOST, 'on' if enabled else 'off')

    @classmethod
    def set_fan_mode(cls, mode) -> None:
        supported = cls._read(cls._AVAILABLE_FAN_MODES).split()
        if mode not in supported:
            raise ValueError(f'Unsupported fan mode: {mode}')
        cls._write(cls._FAN_MODE, mode)

    @classmethod
    def set_shift_mode(cls, mode) -> None:
        supported = cls._read(cls._AVAILABLE_SHIFT_MODES).split()
        if mode not in supported:
            raise ValueError(f'Unsupported shift mode: {mode}')
        cls._write(cls._SHIFT_MODE, mode)
