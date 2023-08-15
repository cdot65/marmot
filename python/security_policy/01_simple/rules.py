# standard library imports
import logging

# 3rd party imports
from config import settings
from panos.panorama import (
    DeviceGroup,
    Panorama,
)
from panos.policies import (
    PreRulebase,
    PostRulebase,
    SecurityRule,
)
from panos.errors import PanDeviceError


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

# ----------------------------------------------------------------------------
# create device group and rulebase objects, build relationships
# ----------------------------------------------------------------------------

# declare our DeviceGroup as DataCenter
device_group = DeviceGroup("DataCenter")

# pass Panorama information into device group
pan.add(device_group)
logging.info("Successfully attached DataCenter device group object to Panorama object")

# create pre_rulebase object, attach to device group, refresh rules
pre_rulebase = PreRulebase()
device_group.add(pre_rulebase)
pre_rules = SecurityRule.refreshall(pre_rulebase)
logging.info("Successfully pulled existing PreRules from DataCenter device group")

# debug will print out each of the rules to the console
for each in pre_rules:
    logging.debug(each)

# create pre_rulebase object, attach to device group, refresh rules
post_rulebase = PostRulebase()
device_group.add(post_rulebase)
post_rules = SecurityRule.refreshall(post_rulebase)
logging.info("Successfully pulled existing PostRules from DataCenter device group")

# debug will print out each of the rules to the console
for each in post_rules:
    logging.debug(each)

# ----------------------------------------------------------------------------
# create a new rule, attach to pre_rulebase, commit to Panorama
# ----------------------------------------------------------------------------
new_rule = SecurityRule(
    name="Allow-HTTP",
    fromzone=["LAN"],
    source=["any"],
    tozone=["WAN_MPLS"],
    destination=["any"],
    application=["web-browsing"],
    service=["application-default"],
    action="allow",
    log_end=True,
    log_setting="Cortex CDL",
    description="Allow HTTP traffic from LAN to WAN",
)

# add new rule to pre_rulebase
pre_rulebase.add(new_rule)

# push new rule to Panorama
new_rule.create()

# ----------------------------------------------------------------------------
# Begin committing our changes to Panorama and remote device groups
# ----------------------------------------------------------------------------
# commit changes to Panorama
pan.commit(sync=True)
logging.info("Successfully committed new rule to Panorama")

# Push the configuration to the remote firewall device groups
pan.commit_all(sync=True, devicegroup=device_group.name)
logging.info("Configuration pushed to device group: %s", device_group.name)
