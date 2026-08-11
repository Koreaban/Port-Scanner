import socket
import time
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from port import all_scan, range_scan, one_scan
from text import get_interface
ports = [21, 22, 25, 80, 110, 443, 8080]
ports_secret = ["21 - FTP, 22 - SSH, 25 - SMTP, 80 - HTTP, 110 - POP, 443 - HTTPS, 8080 - HTTP-Alternate"]

hello, i_can = get_interface()

def hello_function(hello, i_can):
    while True:
        print(hello)
        try:
            final = int(input("Type the nubmer: "))

        except ValueError:
            print("Please enter a valid number.")
            continue

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
while True:
    port = input("Enter the port/all or diaposon wiht '-'  ports of target site: ")
    if port in ["all"] or "-" in port or port.isdigit():
        break
    else:
        print("Please enter 'all' or a valid port number or a range with '-'")
        continue

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

        else:
            try:
                banner = s.recv(1024)

                service_banner = banner.decode(errors="ignore")

            except socket.timeout:
                pass

    else:
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
    all_scan(ip, target, ports, scan_port),

elif "-" in port:
    range_scan(ip, target, port, scan_port)

else:
    one_scan(ip, target, port, scan_port)
