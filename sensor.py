"""Platform for Ethermine Monitor integration."""
import logging

import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.util import Throttle
from homeassistant.helpers.entity import Entity
from homeassistant.components.sensor import (
  PLATFORM_SCHEMA,
  SensorEntity,
)
from homeassistant.const import (
  CONF_NAME,
  CONF_ADDRESS,
  CONF_ICON,
)

from .ethermineApi import EthermineApi
from .const import (
  DOMAIN,
  PLATFORMS,
  MIN_TIME_BETWEEN_UPDATES,
  SENSOR_ACTIVE_WORKERS,
  SENSOR_UNPAID,
  SENSOR_ESTIMATES_EARNINGS,
  SENSOR_CURRENT_HASHRATE,
  SENSOR_AVERAGE_HASHRATE,
  SENSOR_REPORTED_HASHRATE,
  SENSOR_VALID_SHARES,
  SENSOR_STALE_SHARES,
  SENSOR_INVALID_SHARES,
  SENSOR_TYPES,
)

_LOGGER = logging.getLogger(__name__)

# Validation of the user's configuration
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
  vol.Required(CONF_NAME): cv.string,
  vol.Required(CONF_ADDRESS): cv.string,
})

SCAN_INTERVAL = MIN_TIME_BETWEEN_UPDATES

def setup_platform(hass, config, add_entities, discovery_info=None):
  """Set up the Ethermine Monitor platform."""
  # Assign configuration variables.
  # The configuration check takes care they are present.
  _LOGGER.debug("Adding %s...", config[CONF_NAME])
  buffer = EthermineBuffer(EthermineApi(), config)

  sensors = [
    EthermineMonitorSensor(buffer, config, SENSOR_ACTIVE_WORKERS),
    EthermineMonitorSensor(buffer, config, SENSOR_UNPAID),
    EthermineMonitorSensor(buffer, config, SENSOR_ESTIMATES_EARNINGS),
    EthermineMonitorSensor(buffer, config, SENSOR_CURRENT_HASHRATE),
    EthermineMonitorSensor(buffer, config, SENSOR_AVERAGE_HASHRATE),
    EthermineMonitorSensor(buffer, config, SENSOR_REPORTED_HASHRATE),
    EthermineMonitorSensor(buffer, config, SENSOR_VALID_SHARES),
    EthermineMonitorSensor(buffer, config, SENSOR_STALE_SHARES),
    EthermineMonitorSensor(buffer, config, SENSOR_INVALID_SHARES),
  ]
  add_entities(sensors)

class EthermineMonitorSensor(Entity):
  """Representation of an Ethermine Monitor Sensor."""

  def __init__(self, buffer, config, sensor_type):
    """Initialize an EthermineMonitor."""
    self._buffer = buffer
    self._name = config[CONF_NAME]
    self._address = config[CONF_ADDRESS]
    self._sensor_type = sensor_type
    self._state = None
    self._unit_of_measurement = SENSOR_TYPES[sensor_type][1]
    self._attr = {CONF_ADDRESS: config[CONF_ADDRESS], CONF_ICON: SENSOR_TYPES[sensor_type][2]}

  def update(self):
    """Fetch new state data for the sensor."""
    self._buffer.update()
    data = self._buffer.data
    self._state = data[self._sensor_type]
    _LOGGER.debug("%s = %.1f", self._sensor_type, self._state)

  @property
  def name(self):
    """Return the display name of this sensor."""
    return f"{self._name} {SENSOR_TYPES[self._sensor_type][0]}"

  @property
  def state(self):
    """Return the state of the sensor."""
    return self._state

  @property
  def unit_of_measurement(self):
    """Return the unit of measurement of this entity, if any."""
    return self._unit_of_measurement

  @property
  def extra_state_attributes(self):
      """Return the state attributes of the device."""
      return self._attr

class EthermineBuffer:
  """Get the latest data from the api."""

  def __init__(self, api, config):
    """Initialize the sensor."""
    self._api = api
    self._config = config
    self.data = {}

  @Throttle(MIN_TIME_BETWEEN_UPDATES)
  def update(self):
    """Get the latest data."""
    payouts = self._api.getDashboardPayouts(self._config[CONF_ADDRESS])
    dashboard = self._api.getDashboard(self._config[CONF_ADDRESS])
    _LOGGER.debug("Calling getDashboardPayouts API")
    self.data[SENSOR_ACTIVE_WORKERS] = dashboard['currentStatistics']['activeWorkers']
    self.data[SENSOR_UNPAID] = round(dashboard['currentStatistics']['unpaid']/1000000000000000000, 5)
    self.data[SENSOR_ESTIMATES_EARNINGS] = round(payouts['estimates']['coinsPerMin']*1440, 5)
    self.data[SENSOR_CURRENT_HASHRATE] = round(dashboard['currentStatistics']['currentHashrate']/1000000, 3)
    self.data[SENSOR_AVERAGE_HASHRATE] = round(payouts['estimates']['averageHashrate']/1000000, 3)
    self.data[SENSOR_REPORTED_HASHRATE] = round(dashboard['currentStatistics']['reportedHashrate']/1000000, 3)
    self.data[SENSOR_VALID_SHARES] = dashboard['currentStatistics']['validShares']
    self.data[SENSOR_STALE_SHARES] = dashboard['currentStatistics']['staleShares']
    self.data[SENSOR_INVALID_SHARES] = dashboard['currentStatistics']['invalidShares']
