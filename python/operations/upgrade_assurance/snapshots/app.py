from config import settings
from panos_upgrade_assurance.check_firewall import CheckFirewall
from panos_upgrade_assurance.firewall_proxy import FirewallProxy
from panos_upgrade_assurance.snapshot_compare import SnapshotCompare
from panos_upgrade_assurance.utils import printer


dcnpaf1 = FirewallProxy(
    hostname=settings.dcnpaf1.hostname,
    api_key=settings.dcnpaf1.api_key
)

checks_a = CheckFirewall(dcnpaf1)

magpaf1 = FirewallProxy(
    hostname=settings.magpaf1.hostname,
    api_key=settings.magpaf1.api_key
)

checks_b = CheckFirewall(magpaf1)

snapshot_a = checks_a.run_snapshots(['license'])
snapshot_b = checks_b.run_snapshots(['license'])

diff_obj = SnapshotCompare(snapshot_a, snapshot_b)
license_diff = diff_obj.compare_snapshots([{
    'license': {
        'properties': ['!serial']
    }
}])

if not license_diff['license']['changed']['passed']:
    printer(license_diff['license']['changed']['changed_raw'])
    # ... code that handles failed check
