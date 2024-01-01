import pexpect
import logging
from homeassistant.components.switch import SwitchEntity
from homeassistant.const import CONF_MAC

_LOGGER = logging.getLogger(__name__)

DOMAIN = "mibox_socket"

def setup_platform(hass, config, add_entities, discovery_info=None):

    """Set up the Bluetooth Socket switch."""
    _LOGGER.debug("Config received: %s", config)

    device_config = config.get("device", {})
    _LOGGER.debug("Device config: %s", device_config)
    
    mac_address = device_config.get("mac")

    if mac_address is None:
        _LOGGER.error("Incomplete configuration. Please provide 'mac' in the configuration.")
        return

    switch = BluetoothSocketSwitch(mac_address)
    add_entities([switch])

class BluetoothSocketSwitch(SwitchEntity):
    def __init__(self, mac_address):
        self._mac_address = mac_address
        self._state = False

    @property
    def name(self):
        """Return the name of the switch."""
        return f"{DOMAIN}_switch"


    def turn_on(self, **kwargs):
        """Turn on the switch."""
        _LOGGER.debug("Turning on the switch")


        # Spawn a new process (bluetoothctl)
        child = pexpect.spawn('bluetoothctl', timeout=10)

        try:
            # Expect prompt to appear
            child.expect(r'\[bluetooth\]')
            _LOGGER.info("bluetoothctl Started")

            child.sendline('scan on')
            _LOGGER.info("Bluetooth scan on started")
            # Expect output for devices discovered during the scan
            child.expect(r'Discovery started')

            # Wait for some time to allow devices to be discovered
            child.expect(pexpect.TIMEOUT, timeout=10)

            # Stop scanning
            child.sendline('scan off')
            _LOGGER.info("Bluetooth scan off started")
            child.expect(r'Discovery stopped')

            # Use the MAC address variable
            child.sendline(f'pair {self._mac_address}')
            _LOGGER.info("Bluetooth pairing started")
            # Expect output indicating the pairing process

            # Wait for some time to allow pairing to complete
            child.expect(pexpect.TIMEOUT, timeout=10)

            # Expect the 'bluetoothctl>' prompt again
            child.expect(r'bluetoothctl>')
            child.close()
            _LOGGER.info("Bluetooth device paired successfully.")
            
        except Exception as e:
            _LOGGER.error("Error pairing with Bluetooth device: %s", str(e))



    def turn_off(self, **kwargs):
        """Turn off the switch."""
        # Implement turn off logic if needed
        pass

    @property
    def is_on(self):
        """Return true if switch is on."""
        return self._state
