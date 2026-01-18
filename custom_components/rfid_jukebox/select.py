"""Select entity for RFID Jukebox."""
import logging
from homeassistant.components.select import SelectEntity
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
    """Set up the RFID Jukebox select entities."""
    jukebox = hass.data[DOMAIN][entry.entry_id]
    
    media_type_select = RFIDJukeboxMediaTypeSelect(jukebox, entry)
    jukebox.media_type_entity = media_type_select
    
    async_add_entities([media_type_select])


class RFIDJukeboxMediaTypeSelect(SelectEntity):
    """Select entity for choosing media type (playlist, folder, or radio)."""

    def __init__(self, jukebox, entry: ConfigEntry):
        """Initialize the select entity."""
        self._jukebox = jukebox
        self._entry = entry
        self._attr_name = "RFID Jukebox Media Type"
        self._attr_unique_id = f"{entry.entry_id}_media_type"
        # MODIFICATION : Ajout de "radio" dans les options
        self._attr_options = ["playlist", "folder", "radio"]
        self._attr_current_option = "folder"

    @property
    def device_info(self):
        """Return device information."""
        return {
            "identifiers": {(DOMAIN, self._entry.entry_id)},
            "name": "RFID Jukebox",
            "manufacturer": "Custom",
            "model": "RFID Jukebox",
        }

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        self._attr_current_option = option
        self.async_write_ha_state()
        _LOGGER.debug("Media type changed to: %s", option)

    def update_option(self, option: str) -> None:
        """Update the current option from external source."""
        if option in self._attr_options:
            self._attr_current_option = option
            self.async_write_ha_state()
