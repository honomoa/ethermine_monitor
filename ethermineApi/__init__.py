""" Ethermine api """
import logging, requests, json

from .const import BASE_URL
from . import urls

_LOGGER = logging.getLogger(__name__)

class EthermineApi():
  def __init__(self):
    self.host = BASE_URL

  def getDashboardPayouts(self, address):
    response = requests.get(urls.dashboardPayouts(address))
    response.raise_for_status()
    jsonResp = response.json()
    self._payouts = jsonResp
    return jsonResp['data']

  def getDashboard(self, address):
    response = requests.get(urls.dashboard(address))
    response.raise_for_status()
    jsonResp = response.json()
    self._payouts = jsonResp
    return jsonResp['data']
