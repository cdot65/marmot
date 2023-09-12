from config import settings
from panos_upgrade_assurance.firewall_proxy import FirewallProxy
from panos_upgrade_assurance.check_firewall import CheckFirewall

firewall = FirewallProxy(
    hostname=settings.dcnpaf1.hostname, api_key=settings.dcnpaf1.api_key
)

checks = CheckFirewall(firewall)
tests = [
    "active_support",
    "candidate_config",
    "expired_licenses",
    "ntp_sync",
    "panorama",
    # tests below have optional configuration
    {
        "certificates_requirements": {
            "ecdsa": {"hash_method": "sha512"},
            "rsa": {"key_size": 1024, "hash_method": "sha1"},
        }
    },
    {"content_version": {"version": "8634-7678"}},
    {"expired_licenses": {"skip_licenses": ["Threat Prevention"]}},
    {"free_disk_space": {"image_version": "10.1.6-h6"}},
    {"ha": {"skip_config_sync": True}},
    {"planes_clock_sync": {"diff_threshold": 30}},
    # tests below require additional configuration
    {"arp_entry_exist": {"ip": "10.0.1.12"}},
    {"ip_sec_tunnel_status": {"tunnel_name": "ipsec_tun"}},
    {
        "session_exist": {
            "source": "192.168.0.100",
            "destination": "172.16.0.17",
            "dest_port": "443",
        }
    },
]

results = checks.run_readiness_checks(tests)

passed = True

for check in tests:
    check_name = list(check.keys())[0]
    passed = passed & results[check_name]["state"]

    if not results[check_name]["state"]:
        print(f'FAILED: {check_name} - {results[check_name]["reason"]}')

if not passed:
    exit(1)
