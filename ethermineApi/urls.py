""" Ethermine api """

from .const import BASE_URL

def dashboardPayouts(address):
  url = f"{BASE_URL}/miner/{address}/dashboard/payouts"
  return url

def dashboard(address):
  url = f"{BASE_URL}/miner/{address}/dashboard"
  return url
