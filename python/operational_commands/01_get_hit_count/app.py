# standard library imports
import logging
import xml.etree.ElementTree as ET

# 3rd party imports
import xmltodict
from config import settings
from panos.errors import PanDeviceError
from panos.firewall import Firewall
from panos.panorama import (
    Panorama,
)

# ----------------------------------------------------------------------------
# Configure logging
# ----------------------------------------------------------------------------
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s"
)

# ----------------------------------------------------------------------------
# create a panorama object
# ----------------------------------------------------------------------------
pan = Panorama(
    hostname=settings.panorama.base_url,
    api_key=settings.api_key,
)

# ----------------------------------------------------------------------------
# test our Panorama creds, attempt to refresh the system info with pan object
# ----------------------------------------------------------------------------
try:
    pan.refresh_system_info()
    logging.info("Successfully connected to Panorama with credientials")
except PanDeviceError as pan_device_error:
    logging.error("Failed to connect to Panorama: %s", pan_device_error)


datacenter = Firewall(serial="021201090922")
pan.add(datacenter)

hit_count = datacenter.op(
    'show running rule-use hit-count rule-base "security" vsys "vsys1" rules rule-name "VPN Clients to LAN network"'
)

result_xml = ET.tostring(hit_count, encoding="utf-8").decode("utf-8")
result_dict = xmltodict.parse(result_xml)
logging.info(result_dict)
