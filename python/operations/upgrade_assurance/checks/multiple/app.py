from config import settings
from panos_upgrade_assurance.firewall_proxy import FirewallProxy
from panos_upgrade_assurance.check_firewall import CheckFirewall

firewall = FirewallProxy(
    hostname=settings.dcnpaf1.hostname,
    api_key=settings.dcnpaf1.api_key
)

checks = CheckFirewall(firewall)
tests = [
    {'session_exist': {'destination': '172.16.0.17', 'source': '192.168.0.100', 'dest_port': '443'}},
    {'arp_entry_exist': {'ip': '10.1.1.132'}}
]

results = checks.run_readiness_checks(tests)

passed = True

for check in tests:
    check_name = list(check.keys())[0]
    passed = passed & results[check_name]['state']

    if not results[check_name]['state']:
        print(f'FAILED: {check_name} - {results[check_name]["reason"]}')

if not passed:
    exit(1)
