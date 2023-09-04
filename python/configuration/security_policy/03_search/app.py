# standard library imports
import logging
import os
import argparse

# 3rd party imports
from config import settings
import pandas as pd
from tabulate import tabulate
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


def create_panorama_object():
    # create a panorama object
    pan = Panorama(
        hostname=settings.panorama.base_url,
        api_key=settings.api_key,
    )

    # test our Panorama creds, attempt to refresh the system info with pan object
    try:
        pan.refresh_system_info()
        logging.info("Successfully connected to Panorama with credientials")
        return pan
    except PanDeviceError as pan_device_error:
        logging.info("Failed to connect to Panorama: %s", pan_device_error)
        return None


def grab_config():
    """
    Collect configuration objects from Panorama.

    This function retrieves various components of a Panorama configuration including
    Device Groups, Address Groups, and Address Objects. It appends the found address objects
    and address groups into corresponding lists for shared and device group-specific configurations.

    Returns:
        tuple: A tuple containing address_groups and address_objects.
    """


policy = {
    "shared": {"name": "shared", "rules": {"pre_rules": [], "post_rules": []}},
    "device_group": [{"name": "", "rules": {"pre_rules": [], "post_rules": []}}],
}
# refreshall() lets us pull all of object type and attach as child elements
DeviceGroup.refreshall(pan)

for each in pan.children:
    if type(each) == DeviceGroup:
        # print message to console
        logging.info(f"Object {each.name} is a DeviceGroup")

        # begin pre-rulebase
        pre_rulebase = PreRulebase()
        each.add(pre_rulebase)
        pre_rules = SecurityRule.refreshall(pre_rulebase)

        # begin post-rulebase
        post_rulebase = PostRulebase()
        each.add(post_rulebase)
        post_rules = SecurityRule.refreshall(post_rulebase)

        # update our policy dictionary
        policy["device_group"].append(
            {
                "name": each.name,
                "rules": {
                    "pre_rules": pre_rules,
                    "post_rules": post_rules,
                },
            }
        )
    else:
        print(f"Object is not a DeviceGroup")

# how to attach on to an existing object in the local python config
datacenter = pan.find("DataCenter", DeviceGroup)

# let's pull existing pre-rules for our devicegroup
pre_rulebase = PreRulebase()
datacenter.add(pre_rulebase)
pre_rules = SecurityRule.refreshall(pre_rulebase)


def find_matches(address_groups, address_objects, search):
    """
    Find all associations of an address object.

    This function takes the address groups, address objects, and a search string to find all
    associations of a given address object. It returns the associations found.

    Args:
        address_groups (list): A list of address groups.
        address_objects (list): A list of address objects.
        search (str): The search string for finding associations.

    Returns:
        list: A list of associations found.
    """
    # ...
    # The existing code
    # ...

    # create a dictionary of empty lists to present potential matches
    potential_matches = {"fromzone": [], "tozone": [], "service": [], "application": []}

    # loop over our pre_rules and add those that match aspect
    for each in pre_rules:
        if "VPN" in each.fromzone:
            potential_matches["fromzone"].append(each.name)
        if "DMZ" in each.tozone:
            potential_matches["tozone"].append(each.name)

    target_string = "LAN to Synology"
    count = 0

    for key, values in potential_matches.items():
        count += values.count(target_string)

    logging.info(f"The criteria '{target_string}' appears {count} times.")


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
    )

    pan = create_panorama_object()

    if type(pan) != Panorama:
        logging.debug("Failed to create Panorama object")
    else:
        logging.debug("Successfully created Panorama object")

    main(pan)
