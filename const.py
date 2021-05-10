"""Contants for Ethermine Monitor integration"""
from datetime import timedelta

DOMAIN = "ethermine_monitor"
PLATFORMS = ["sensor"]

MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=30)
SENSOR_ESTIMATES_EARNINGS = "estimates_earnings"
SENSOR_AVERAGE_HASHRATE = "average_hashrate"
SENSOR_UNPAID = "unpaid_balance"
SENSOR_ACTIVE_WORKERS = "active_workers"
SENSOR_REPORTED_HASHRATE = "reported_hashrate"
SENSOR_CURRENT_HASHRATE = "current_hashrate"
SENSOR_VALID_SHARES = "valid_shares"
SENSOR_STALE_SHARES = "stale_shares"
SENSOR_INVALID_SHARES = "invalid_shares"
UNIT_ETH = "ETH"
UNIT_MHS = "Mh/s"
UNIT_SHARES = "Shares"

SENSOR_TYPES = {
  SENSOR_ESTIMATES_EARNINGS: ["Estimates Earnings", UNIT_ETH, "mdi:ethereum"],
  SENSOR_AVERAGE_HASHRATE: ["Average Hashrate", UNIT_MHS, "mdi:pound"],
  SENSOR_UNPAID: ["Unpaid Balance", UNIT_ETH, "mdi:ethereum"],
  SENSOR_ACTIVE_WORKERS: ["Active Workers", "", "mdi:account-hard-hat"],
  SENSOR_REPORTED_HASHRATE: ["Reported Hashrate", UNIT_MHS, "mdi:pound"],
  SENSOR_CURRENT_HASHRATE: ["Current Hashrate", UNIT_MHS, "mdi:pound"],
  SENSOR_VALID_SHARES: ["Valid Shares", UNIT_SHARES, "mdi:mine"],
  SENSOR_STALE_SHARES: ["Stale Shares", UNIT_SHARES, "mdi:mine"],
  SENSOR_INVALID_SHARES: ["Invalid Shares", UNIT_SHARES, "mdi:mine"],
}
