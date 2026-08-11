import json
from concurrent.futures import ThreadPoolExecutor

def all_scan(ip, target, ports, scan_port):
    results = []
    futures =  []
    with ThreadPoolExecutor(max_workers=7) as executor:
            for p in ports:
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

            return results

def range_scan(ip, target, ports, port, scan_port):
      results = []
      futures = []
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
      return results


def one_scan(ip, target, port, scan_port):
    try:
        port = int(port)

        result = scan_port(ip, target, port)

        print(
            f"{result['port']} {result['port service']} - "
            f"{result['status']} "
            f"({result['response_time_ms']} ms)"
        )
        with open("scan.json", "w") as file:
            json.dump(result, file, indent=4)
        return result
    except ValueError:
        print("Invalid port number")