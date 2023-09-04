from config import settings
from panos_upgrade_assurance.firewall_proxy import FirewallProxy
from panos_upgrade_assurance.check_firewall import CheckFirewall


firewall = FirewallProxy(
    hostname=settings.dcnpaf1.hostname,
    api_key=settings.dcnpaf1.api_key
)

checks = CheckFirewall(firewall)

checks_configuration = [
    {'session_exist': {
        'source': '10.1.1.12',
        'destination': '10.0.0.1',
        'dest_port': '8080'
    }},
    {'arp_entry_exist': {
        'ip': '10.1.1.12'
    }},
]

results = checks.run_readiness_checks(checks_configuration)

print(results)
