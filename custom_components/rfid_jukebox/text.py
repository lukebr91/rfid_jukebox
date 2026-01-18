"""Text entities for RFID Jukebox."""
import logging
from homeassistant.components.text import TextEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the RFID Jukebox text entities."""
    jukebox = hass.data[DOMAIN][entry.entry_id]
    
    text_entity = RFIDJukeboxMediaNameText(jukebox, entry)
    alias_entity = RFIDJukeboxAliasText(jukebox, entry)
    last_tag_entity = RFIDJukeboxLastTagText(jukebox, entry)
    
    jukebox.text_entity = text_entity
    jukebox.alias_entity = alias_entity
    
    async_add_entities([text_entity, alias_entity, last_tag_entity])


class RFIDJukeboxMediaNameText(TextEntity):
    """Text entity for entering media name or URI."""

    def __init__(self, jukebox, entry: ConfigEntry):
        """Initialize the text entity."""
        self._jukebox = jukebox
        self._entry = entry
        self._attr_name = "RFID Jukebox Media Name"
        self._attr_unique_id = f"{entry.entry_id}_media_name"
        self._attr_icon = "mdi:music-box"
        self._attr_native_value = ""

    @property
    def device_info(self):
        """Return device information."""
        return {
            "identifiers": {(DOMAIN, self._entry.entry_id)},
            "name": "RFID Jukebox",
            "manufacturer": "Custom",
            "model": "RFID Jukebox",
        }

    async def async_set_value(self, value: str) -> None:
        """Update the current value."""
        self._attr_native_value = value
        self.async_write_ha_state()

    def update_value(self, value: str) -> None:
        """Update the value from external source."""
        self._attr_native_value = value
        self.async_write_ha_state()


class RFIDJukeboxAliasText(TextEntity):
    """Text entity for entering tag alias."""

    def __init__(self, jukebox, entry: ConfigEntry):
        """Initialize the text entity."""
        self._jukebox = jukebox
        self._entry = entry
        self._attr_name = "RFID Jukebox Alias"
        self._attr_unique_id = f"{entry.entry_id}_alias"
        self._attr_icon = "mdi:label"
        self._attr_native_value = ""

    @property
    def device_info(self):
        """Return device information."""
        return {
            "identifiers": {(DOMAIN, self._entry.entry_id)},
            "name": "RFID Jukebox",
            "manufacturer": "Custom",
            "model": "RFID Jukebox",
        }

    async def async_set_value(self, value: str) -> None:
        """Update the current value."""
        self._attr_native_value = value
        self.async_write_ha_state()

    def update_value(self, value: str) -> None:
        """Update the value from external source."""
        self._attr_native_value = value
        self.async_write_ha_state()


class RFIDJukeboxLastTagText(TextEntity):
    """Text entity showing the last scanned tag."""

    def __init__(self, jukebox, entry: ConfigEntry):
        """Initialize the text entity."""
        self._jukebox = jukebox
        self._entry = entry
        self._attr_name = "RFID Jukebox Last Tag"
        self._attr_unique_id = f"{entry.entry_id}_last_tag"
        self._attr_icon = "mdi:tag"
        self._attr_native_value = ""
        self._attr_entity_registry_enabled_default = True

    @property
    def device_info(self):
        """Return device information."""
        return {
            "identifiers": {(DOMAIN, self._entry.entry_id)},
            "name": "RFID Jukebox",
            "manufacturer": "Custom",
            "model": "RFID Jukebox",
        }

    async def async_set_value(self, value: str) -> None:
        """Update the current value."""
        self._attr_native_value = value
        self._jukebox.last_tag = value
        self.async_write_ha_state()

    @property
    def native_value(self) -> str:
        """Return the current tag value."""
        return self._jukebox.last_tag or ""
