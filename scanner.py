import socket
import time
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor

ports = [21, 22, 25, 80, 110, 443, 8080]
ports_secret = ["21 - FTP, 22 - SSH, 25 - SMTP, 80 - HTTP, 110 - POP, 443 - HTTPS, 8080 - HTTP-Alternate"]

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
def hello_function(hello, i_can):
    while True:
        print(hello)
        final = int(input("Type the nubmer: "))

        if final == 1:
            while True:
                target  = input("Enter the name of site: ")

                try:
                    ip = socket.gethostbyname(target)
                    print(f"IP address is {ip}\n")
                    return ip, target

                except socket.gaierror:
                    print("Invailid IP address or Domain")
        elif final == 99:
            print(i_can)
        elif final == 0:
            print("Goodbye!")
            sys.exit()
        else:
            print("Please enter 1 or 99: ")

ip, target = hello_function(hello, i_can)

print(f"{ports_secret}\nChoose the ports or write 'all' for scanning all of ports, you also can write diaposon whith '-'")
port = input("Enter the port/all or diaposon wiht '-'  ports of target site: ")

def scan_port(ip, target, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)

    start = time.perf_counter()

    result = s.connect_ex((ip,port))

    end = time.perf_counter()

    time_result = (end - start) * 1000

    http_banner = None
    service_banner = None

    try:
        servbyport = socket.getservbyport(port)
    except OSError:
        servbyport = "Unknown"

    if result == 0:
        print(f"{port} - {servbyport} is \033[92mopen\033[0m, connectoin time: {time_result:.2f} ms")
        status = "Open"

        if port in (80, 8080):
            request = (
                f"HEAD / HTTP/1.1\r\n"
                f"Host: {target}\r\n"
                f"Connection: close\r\n\r\n"
            )

            s.send(request.encode())
            response = s.recv(4096)

            http_banner = response.decode(errors="ignore")

            print(http_banner)

        else:
            try:
                banner = s.recv(1024)

                service_banner = banner.decode(errors="ignore")

                print(service_banner)
            except socket.timeout:
                print("No banner received")

    else:
        print(f"{port} {servbyport} - is \033[31mclose\033[0m")
        print(f"Error code - {result}")
        print(f"Description: {os.strerror(result)}")
        status = "Close"

    result_json = {
           "target": target,
           "ip": ip,
           "port": port,
           "port service": servbyport,
           "status": status,
           "status code": result,
           "Description error": os.strerror(result),
           "response_time_ms": round(time_result, 2),
           "HTTP-banner": http_banner,
           "banner": service_banner
    }

    s.close()
    return result_json

results = []
futures = []
if port == 'all':
    with ThreadPoolExecutor(max_workers=7) as executor:
        for p in ports:
            futures.append(executor.submit(scan_port, ip, target, p))

        for future in futures:
            results.append(future.result())

            results.sort(key=lambda x:["port"])

        for result in results:
                   print(
                       f"{result['port']} {result['port service']} - "
                       f"{result['status']} "
                       f"({result['response_time_ms']} ms)"
                   )
        with open("scan.json", "w") as file:
            json.dump(results, file, indent=4)

elif "-" in port:
    try:
        start, end = port.split("-")

        start = int(start)
        end = int(end)
        
        if start > end:
            print("Start port must be less than end port")

        else:
            with ThreadPoolExecutor(max_workers=10) as executor:

               for p in range(start, end +1):
                  futures.append(executor.submit(scan_port, ip, target, p))

               for future in futures:
                   results.append(future.result())

                   results.sort(key=lambda x: x["port"])
               for result in results:
                   print(
                       f"{result['port']} {result['port service']} - "
                       f"{result['status']} "
                       f"({result['response_time_ms']} ms)"
                   )
               with open("scan.json", "w") as file:
                   json.dump(results, file, indent=4)

    except ValueError:
        print("Incorrect range")

else:
    try:
        port = int(port)

        result = scan_port(ip, target, port)

        results.append(result)

        for result in results:
            print(
                f"{result['port']} {result['port service']} - "
                f"{result['status']} "
                f"({result['response_time_ms']} ms)"
            )
        with open("scan.json", "w") as file:
            json.dump(results, file, indent=4)
    except ValueError:
        print(f"{port} is incorrect")
