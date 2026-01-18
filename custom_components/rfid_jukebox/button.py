"""Button entities for RFID Jukebox."""
import logging
from homeassistant.components.button import ButtonEntity
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
    """Set up the RFID Jukebox button entities."""
    jukebox = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([RFIDJukeboxMapButton(jukebox, entry)])


class RFIDJukeboxMapButton(ButtonEntity):
    """Button to map the current tag to media."""

    def __init__(self, jukebox, entry: ConfigEntry):
        """Initialize the button."""
        self._jukebox = jukebox
        self._entry = entry
        self._attr_name = "RFID Jukebox Map Tag"
        self._attr_unique_id = f"{entry.entry_id}_map_tag"
        self._attr_icon = "mdi:tag-plus"

    @property
    def device_info(self):
        """Return device information."""
        return {
            "identifiers": {(DOMAIN, self._entry.entry_id)},
            "name": "RFID Jukebox",
            "manufacturer": "Custom",
            "model": "RFID Jukebox",
        }

    async def async_press(self) -> None:
        """Handle the button press to map a tag."""
        if not self._jukebox.last_tag:
            _LOGGER.warning("No tag has been scanned yet. Scan a tag first.")
            return

        tag_id = self._jukebox.last_tag
        
        # Get the media type from the select entity
        media_type = "folder"
        if self._jukebox.media_type_entity:
            media_type = self._jukebox.media_type_entity.current_option

        # Get the alias from the alias text entity
        alias = tag_id
        if self._jukebox.alias_entity:
            alias = self._jukebox.alias_entity.native_value or tag_id

        # MODIFICATION : Gérer différemment selon le type
        if media_type == "radio":
            # Pour les radios, on récupère l'URI depuis le text_entity
            uri = None
            if self._jukebox.text_entity:
                uri = self._jukebox.text_entity.native_value
            
            if not uri:
                _LOGGER.error("No URI provided for radio mapping. Please enter a URI (e.g., library://radio/7)")
                return
            
            _LOGGER.info("Mapping tag '%s' to radio URI: %s", tag_id, uri)
            await self._jukebox.async_map_tag(
                tag_id=tag_id,
                media_type=media_type,
                media_name=None,
                alias=alias,
                uri=uri
            )
        else:
            # Pour playlist et folder, on utilise le nom
            media_name = None
            if self._jukebox.text_entity:
                media_name = self._jukebox.text_entity.native_value

            if not media_name:
                _LOGGER.error("No media name provided. Please enter a %s name.", media_type)
                return

            _LOGGER.info("Mapping tag '%s' to %s: %s", tag_id, media_type, media_name)
            await self._jukebox.async_map_tag(
                tag_id=tag_id,
                media_type=media_type,
                media_name=media_name,
                alias=alias,
                uri=None
            )
