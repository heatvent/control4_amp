import logging
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.components.media_player import (
    MediaPlayerEntity, MediaPlayerEntityFeature, SOURCE_SELECT)
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.entity import DeviceInfo
from .const import DOMAIN, INPUTS
from .udp_communication import UDPCommunication

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    """Set up Control4 Amp Media Player from a config entry."""
    udp_comm = UDPCommunication(hass, entry.data["ip_address"], entry.data["port"])
    await udp_comm.start()
    name = entry.data.get("name")
    amp = Control4AmpMediaPlayer(name=name, unique_id=f"{entry.entry_id}_amp", device_info={
        "identifiers": {(DOMAIN, f"{entry.entry_id}_amp")},
        "name": name,
        "manufacturer": "Control4",
        "model": "C4-8AMP1-B",
        "sw_version": "1.0",
        "via_device": (DOMAIN, f"{entry.entry_id}")
    }, udp_comm=udp_comm)
    zones = [Control4AmpZoneMediaPlayer(name=f"{name} Zone {i+1}", unique_id=f"{entry.entry_id}_zone{i+1}", device_info={
        "identifiers": {(DOMAIN, f"{entry.entry_id}_zone{i+1}")},
        "name": f"{name} Zone {i+1}",
        "manufacturer": "Control4",
        "model": "Zone Amplifier",
        "sw_version": "1.0",
        "via_device": (DOMAIN, f"{entry.entry_id}_amp"),
        "inputs": INPUTS
    }, udp_comm=udp_comm) for i in range(4)]
    async_add_entities([amp] + zones)

class Control4AmpMediaPlayer(MediaPlayerEntity):
    """A class representing a Control4 Amp media player."""
    def __init__(self, name, unique_id, device_info, udp_comm):
        self._name = name
        self._unique_id = unique_id
        self._device_info = device_info
        self._state = None
        self.udp_comm = udp_comm

    async def async_added_to_hass(self):
        """When entity is added to Home Assistant, request firmware."""
        await super().async_added_to_hass()
        self.udp_comm.request_firmware_version()

    @property
    def unique_id(self):
        """Return a unique identifier for this device."""
        return self._unique_id

    @property
    def device_info(self):
        """Return device information."""
        return self._device_info

    @property
    def name(self):
        """Return the name of the device."""
        return self._name

    @property
    def state(self):
        """Return the state of the device."""
        return self._state

    @property
    def supported_features(self):
        """Return the supported features."""
        return MediaPlayerEntityFeature.PLAY | MediaPlayerEntityFeature.PAUSE

class Control4AmpZoneMediaPlayer(MediaPlayerEntity):
    """A class representing a Control4 Amp Zone media player."""
    def __init__(self, name, unique_id, device_info, udp_comm):
        super().__init__()
        self._name = name
        self._unique_id = unique_id
        self._device_info = device_info
        self._state = None
        self.udp_comm = udp_comm
        self._source = None
        self._source_list = device_info['inputs']

    @property
    def source(self):
        """Return the current source."""
        return self._source

    @property
    def source_list(self):
        """Return the list of available sources."""
        return self._source_list

    @property
    def supported_features(self):
        """Return the supported features."""
        return super().supported_features | SOURCE_SELECT

    def select_source(self, source):
        """Set the input source."""
        self._source = source
        _LOGGER.info(f"Source set to {source} on {self._name}")
        # Here you might add code to communicate the source change to the device.
        self.async_write_ha_state()
