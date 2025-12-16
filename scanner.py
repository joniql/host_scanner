import socket
import ipaddress
import sys
import time
from colorama import Fore
from concurrent.futures import ThreadPoolExecutor

target = sys.argv[1]
ports = [int(p.strip()) for p in sys.argv[2].split(",")]
workerlimit = 50

def main():
    starttime = time.perf_counter()

    targets = build_ip_list(target)

    with ThreadPoolExecutor(max_workers=workerlimit) as exe:
        futures = [
            exe.submit(is_host_alive, ip, ports)
            for ip in targets
        ]

    for _ in futures:
        pass

    endtime = time.perf_counter()
    print(f"Scan completed in {endtime - starttime:.2f} seconds")

def build_ip_list(target):

    if "/" in target:
        net = ipaddress.ip_network(target)
        return list(net.hosts())
    else:
        return [ipaddress.ip_address(target)]
    
def is_host_alive(ip, ports, timeout=1):
    for p in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((str(ip), p))

            if result == 0:
                print (Fore.GREEN + f"[+]{Fore.RESET} {ip} {Fore.BLUE}({p}){Fore.RESET}")
    
main()
