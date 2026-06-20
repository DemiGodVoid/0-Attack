import socket
import threading
import subprocess
RED = "\033[31m"
GREEN = "\033[32m"
BLUE = "\033[34m"
RESET = "\033[0m"


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except:
        ip = None
    finally:
        s.close()
    return ip

def get_network_ips(ip):
    network = ip.rsplit('.', 1)[0]
    return [f"{network}.{i}" for i in range(1, 255)]

def ping(ip):
    try:
        subprocess.check_output(["ping", "-n", "1", "-w", "1000", ip], stderr=subprocess.DEVNULL)
        return True
    except:
        return False

def resolve_hostname(ip):
    try:
        hostname = socket.gethostbyaddr(ip)[0]
        return hostname
    except socket.herror:
        return None

def identify_device(hostname):
    hostname_lower = hostname.lower()
    if "ps5" in hostname_lower or "playstation" in hostname_lower:
        return "PlayStation 5"
    elif "iphone" in hostname_lower:
        return "iPhone"
    elif "android" in hostname_lower:
        return "Android Device"
    elif "camera" in hostname_lower:
        return "Camera"
    elif "tv" in hostname_lower or "smart tv" in hostname_lower:
        return "TV"
    elif "pc" in hostname_lower or "laptop" in hostname_lower:
        return "Computer"
    return "Unknown"

def discover_ssdp():
    message = (
        "M-SEARCH * HTTP/1.1\r\n"
        "HOST:239.255.255.250:1900\r\n"
        "MAN:\"ssdp:discover\"\r\n"
        "MX:1\r\n"
        "ST:urn:schemas-upnp-org:device:MediaRenderer:1\r\n\r\n"
    )
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.settimeout(2)
    sock.sendto(message.encode(), ("239.255.255.250", 1900))
    responses = []
    try:
        while True:
            data, addr = sock.recvfrom(1024)
            responses.append((addr, data.decode()))
    except socket.timeout:
        pass
    sock.close()
    return responses

devices = []

def scan_ip(ip):
    if ping(ip):
        hostname = resolve_hostname(ip)
        device_type = "Unknown"
        if hostname:
            device_type = identify_device(hostname)
        devices.append((ip, hostname or "Unknown", device_type))
        print(f"Active: {ip} - Hostname: {hostname or 'Unknown'} - Device: {device_type}")

def main():
    local_ip = get_local_ip()
    if not local_ip:
        print("Could not determine local IP.")
        return
    print(f"Your local IP: {local_ip}")
    ips = get_network_ips(local_ip)
    print(f"{GREEN}Scanning your network for active devices...")
    threads = []
    for ip in ips:
        t = threading.Thread(target=scan_ip, args=(ip,))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    print("\nActive devices found:")
    for ip, hostname, device_type in devices:
        print(f"{ip} - {hostname} - {device_type}")
    print("\nDiscovering UPnP devices via SSDP...")
    ssdp_responses = discover_ssdp()
    for addr, resp in ssdp_responses:
        print(f"\nSSDP response from {addr}:\n{resp}")


if __name__ == "__main__":
    main()
