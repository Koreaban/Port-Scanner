# Python Port Scanner

A multithreaded port scanner written in Python.

## Features

* Scan a single port
* Scan a range of ports
* Scan predefined common ports
* Multithreaded scanning for faster performance
* Measures connection time for each port
* Detects common services (HTTP, HTTPS, FTP, SSH, SMTP, etc.)
* Attempts to retrieve HTTP and service banners
* Saves scan results to a JSON file

## Technologies

* Python 3
* socket
* concurrent.futures (ThreadPoolExecutor)
* json
* os
* time
* sys

## Usage

Run the program:

```bash
python3 scanner.py
```

The scanner allows you to:

* Scan all predefined ports
* Scan a single port
* Scan a custom port range (e.g. `20-100`)
* Save results to `scan.json`

## Example

```text
21 ftp - Open (12.54 ms)
22 ssh - Close (1001.08 ms)
80 http - Open (45.31 ms)
443 https - Open (39.87 ms)
```

## Project Status

Completed as a learning project.

## Author

Korea
