import logging
from config import settings
from panos.panorama import DeviceGroup, Panorama
from panos.objects import AddressObject, AddressGroup, ServiceObject, Tag
from panos.errors import PanDeviceError
from panos.panorama import PanoramaCommitAll

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)

# create a panorama object
pan = Panorama(
    hostname=settings.panorama.base_url,
    api_key=settings.api_key,
)

# test our Panorama creds, attempt to refresh the system info with pan object
try:
    pan.refresh_system_info()
    logging.info("Successfully connected to Panorama with credientials")
except PanDeviceError as pan_device_error:
    logging.info("Failed to connect to Panorama: %s", pan_device_error)
    pan = None

device_group = DeviceGroup("DataCenter")
pan.add(device_group)
logging.info("Successfully attached to Device Group: %s", device_group.name)

k8s_tag = Tag(
    name="Kubernetes",
    color="color2",
    comments="Tag for all k8s related services",
)

pan.add(k8s_tag)
k8s_tag.update("color")
logging.info("Successfully updated Tag: %s", k8s_tag.name)

k8s_service = ServiceObject(
    name="Kubernetes_MGMT",
    protocol="tcp",
    destination_port="6443",
    description="Default k8s Managment Port",
    tag=["Kubernetes"],
)

device_group.add(k8s_service)
k8s_service.create()
logging.info("Successfully created Service Object: %s", k8s_service.name)

# create the k8s address object
k8s_ao = AddressObject(
    name="DCN-K8S-001",
    value="172.16.0.15",
    description="Kubernetes Cluster",
    tag=["Kubernetes"],
)

device_group.add(k8s_ao)
k8s_ao.update("value")
logging.info("Successfully updated Address Object: %s", k8s_ao.name)

k8s_ao_group = AddressGroup(
    name="k8s_clusters",
    dynamic_value="'Kubernetes'",
    description="Kubernetes Cluster",
    tag=["Kubernetes"],
)

device_group.add(k8s_ao_group)
k8s_ao_group.create()
logging.info("Successfully updated Address Group: %s", k8s_ao_group.name)


# ----------------------------------------------------------------------------
# Authorization config
# ----------------------------------------------------------------------------

# create the Auth tag
auth_tag = Tag(
    name="Auth",
    color="color7",
    comments="Tag for all RADIUS, LDAP, and similar services",
)

pan.add(auth_tag)
auth_tag.create()
logging.info("Successfully created Tag: %s", auth_tag.name)

# create the OpenLDAP service object
oldap_service = ServiceObject(
    name="Open LDAP",
    protocol="tcp",
    destination_port="1389",
    description="Default LDAP Port for OpenLDAP",
    tag=["Kubernetes", "Auth"],
)

device_group.add(oldap_service)
oldap_service.create()
logging.info("Successfully created Service Object: %s", oldap_service.name)


# create the OpenLDAP address object
oldap_ao = AddressObject(
    name="DCN-LDAP-001",
    value="172.16.0.153",
    description="OpenLDAP Server on Kubernetes Cluster",
    tag=["Kubernetes", "Auth"],
)

device_group.add(oldap_ao)
oldap_ao.update("tag")
logging.info("Successfully updated Address Object: %s", oldap_ao.name)

auth_ao_group = AddressGroup(
    name="Authentication Services",
    dynamic_value="'Auth'",
    description="Authorization Services",
    tag=["Auth"],
)

device_group.add(auth_ao_group)
auth_ao_group.create()
logging.info("Successfully created Address Group: %s", auth_ao_group.name)


# ----------------------------------------------------------------------------
# Commit config
# ----------------------------------------------------------------------------
# Create PanoramaCommitAll object targeting the "DataCenter" device group
commit_all_datacenter = PanoramaCommitAll(
    style='device group',
    name='DataCenter',
    description='Committing changes to DataCenter device group'
)

# Perform the commit
pan.commit(cmd=commit_all_datacenter)

print("Commit successful!")
