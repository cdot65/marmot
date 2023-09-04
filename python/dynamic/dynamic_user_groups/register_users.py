import toml
import random
from xml.etree.ElementTree import Element, SubElement, ElementTree

# Read the TOML file
with open("settings.toml") as file:
    data = toml.load(file)

# Create the root element of the XML file
root = Element("uid-message")

# Add child elements
version_elem = SubElement(root, "version")
version_elem.text = "2.0"

type_elem = SubElement(root, "type")
type_elem.text = "update"

payload_elem = SubElement(root, "payload")
register_user_elem = SubElement(payload_elem, "register-user")

# Define the possible member values
members = ["gold", "silver", "bronze", "baddies"]

# Extract usernames and build the XML structure
for login in data["users"]["logins"]:
    username = login["username"].replace(
        "\\\\", "\\"
    )  # Convert double backslash to single
    entry_elem = SubElement(register_user_elem, "entry", {"user": username})
    tag_elem = SubElement(entry_elem, "tag")
    member_elem = SubElement(tag_elem, "member")
    member_elem.text = random.choice(members)  # Randomly select a member value

# Create the ElementTree object
tree = ElementTree(root)

# Write to the XML file
tree.write("dag_users.xml")
