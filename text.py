
def get_interface():
    hello = r"""

===============================================================
                   Python Port Scanner v1.0
===============================================================
 ____            _      _____
|  _ \ ___  _ __| |_   / ____| ___ __ _ _ __  _ __   ___ _ __
| |_) / _ \| '__| __| | (___  / __/ _` | '_ \| '_ \ / _ \ '__|
|  __/ (_) | |  | |_   \___ \| (_| (_| | | | | | | |  __/ |
|_|   \___/|_|   \__|  |____/ \___\__,_|_| |_|_| |_|\___|_|


[1] Start Scan
[99] Help
[0] Exit
================================================================
"""

    i_can = """
================ PORT SCANNER =================

Features:

[✓] Scan domains and IP addresses
[✓] Scan a single port
[✓] Scan all predefined ports
[✓] Scan a custom port range
[✓] Detect open and closed ports
[✓] Identify common services
[✓] Measure response time
[✓] Grab HTTP/service banners
[✓] Save results to JSON
[✓] Multithreaded scanning

===============================================
"""
    return hello, i_can