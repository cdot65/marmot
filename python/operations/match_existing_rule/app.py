# standard library
import logging
import argparse
import xml.etree.ElementTree as ET

# 3rd party
from config import settings
import xmltodict

# palo alto networks
from panos.firewall import Firewall
from panos.panorama import Panorama


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Parse arguments passed from CLI at runtime."
    )
    parser.add_argument(
        "--source-ip",
        dest="source_ip",
    )
    parser.add_argument(
        "--serial",
        dest="serial",
    )
    parser.add_argument(
        "--destination-ip",
        dest="destination_ip",
    )
    parser.add_argument(
        "--source-zone",
        dest="source_zone",
    )
    parser.add_argument(
        "--destination-zone",
        dest="destination_zone",
    )
    parser.add_argument(
        "--application",
        dest="application",
    )
    parser.add_argument(
        "--destination-port",
        dest="destination_port",
    )
    parser.add_argument(
        "--protocol",
        dest="protocol",
    )
    return parser.parse_args()


args = parse_arguments()

# create an instance of the Panorama class
pan = Panorama(hostname=settings.panorama.base_url, api_key=settings.api_key)

# refresh the list of firewalls attached to Panorama
Firewall.refreshall(pan)

# find the firewall with the serial number passed in as an argument
for each in pan.children:
    if isinstance(each, Firewall):
        if each.serial == args.serial:
            target_firewall = each

print(f"target firewall: {target_firewall}")
rule_match_cmd = f'test security-policy-match source "{args.source_ip}" destination "{args.destination_ip}" from "{args.source_zone}" to "{args.destination_zone}" application "{args.application}" destination-port "{args.destination_port}" protocol "{args.protocol}"'

rule_match = target_firewall.op(rule_match_cmd)
result_xml = ET.tostring(rule_match, encoding="utf-8").decode("utf-8")
result_dict = xmltodict.parse(result_xml)
print(result_dict)
