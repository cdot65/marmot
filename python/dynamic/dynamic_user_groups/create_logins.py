from xml.etree.ElementTree import Element, SubElement, ElementTree
from config import settings


# Create the root element of the XML file
root = Element("uid-message")

# Add child elements
type_elem = SubElement(root, "type")
type_elem.text = "update"

payload_elem = SubElement(root, "payload")
login_elem = SubElement(payload_elem, "login")

# Extract usernames and IP addresses and add them as entry elements
for login in settings.users.logins:
    username = login["username"].replace(
        "\\\\", "\\"
    )  # Convert double backslash to single
    ip = login["ipaddr"]
    entry_elem = SubElement(login_elem, "entry", {"name": username, "ip": ip})

# Create the ElementTree object
tree = ElementTree(root)

# Write to the XML file
tree.write("dag_logins.xml")
