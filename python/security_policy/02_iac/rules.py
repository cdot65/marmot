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

# # debug will print out each of the rules to the console
# for each in pre_rules:
#     logging.debug(each)

# Infrastructure-as-Code (IaC) - delete all existing rules for candidate config
for each in pre_rules:
    each.delete()


# create pre_rulebase object, attach to device group, refresh rules
post_rulebase = PostRulebase()
device_group.add(post_rulebase)
post_rules = SecurityRule.refreshall(post_rulebase)
logging.info("Successfully pulled existing PostRules from DataCenter device group")

# debug will print out each of the rules to the console
# for each in post_rules:
#     logging.debug(each)

# Infrastructure-as-Code (IaC) - delete all existing rules for candidate config
for each in post_rules:
    each.delete()

# ----------------------------------------------------------------------------
# create new rules, attach to pre_rulebase, commit to Panorama
# ----------------------------------------------------------------------------
for each in settings.datacenter.security_rules.pre_rules:
    # create new rules based on list of rules in settings.toml
    new_rule = SecurityRule(
        name=each.name,
        fromzone=each.from_zone,
        tozone=each.to_zone,
        source=each.source,
        destination=each.destination,
        application=each.application,
        service=each.service,
        category=each.category,
        action=each.action,
        log_start=each.log_start,
        log_end=each.log_end,
        log_setting=each.log_setting,
        description=each.description,
        tag=each.tag,
    )

    # add new rule to pre_rulebase
    pre_rulebase.add(new_rule)

    # push new rule to Panorama
    new_rule.create()

# ----------------------------------------------------------------------------
# create new rules, attach to post_rulebase, commit to Panorama
# ----------------------------------------------------------------------------
for each in settings.datacenter.security_rules.post_rules:
    # create new rules based on list of rules in settings.toml
    new_rule = SecurityRule(
        name=each.name,
        fromzone=each.from_zone,
        tozone=each.to_zone,
        source=each.source,
        destination=each.destination,
        application=each.application,
        service=each.service,
        category=each.category,
        action=each.action,
        log_start=each.log_start,
        log_end=each.log_end,
        log_setting=each.log_setting,
        description=each.description,
        tag=each.tag,
    )

    # add new rule to pre_rulebase
    post_rulebase.add(new_rule)

    # push new rule to Panorama
    new_rule.create()

# ----------------------------------------------------------------------------
# Make sure there is a default Deny Any at the bottom of the post rulebase
# ----------------------------------------------------------------------------
# find the "Deny Any" rule
deny_all = SecurityRule.find(post_rulebase, name="Deny Any")
deny_all.refresh()

# move rule to the bottom of the post rulebase
deny_all.move(location="bottom")

# ----------------------------------------------------------------------------
# Begin committing our changes to Panorama and remote device groups
# ----------------------------------------------------------------------------
# commit changes to Panorama
# pan.commit(sync=True)
# logging.info("Successfully committed new rule to Panorama")

# Push the configuration to the remote firewall device groups
pan.commit_all(sync=True, devicegroup=device_group.name)
logging.info("Configuration pushed to device group: %s", device_group.name)
