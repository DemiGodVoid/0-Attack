import socket
import requests
import threading
import queue
import whois

def resolve_hostname(hostname):
    try:
        ip = socket.gethostbyname(hostname)
        return ip
    except:
        return None

def get_dns_info(hostname):
    try:
        return socket.gethostbyname_ex(hostname)
    except:
        return None

def get_ip_info(ip):
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json")
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None

def whois_lookup(target):
    try:
        result = whois.whois(target)
        return result
    except:
        return None

def port_scan(ip, port_queue, open_ports):
    while True:
        port = port_queue.get()
        if port is None:
            break
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        try:
            result = sock.connect_ex((ip, port))
            if result == 0:
                open_ports.append(port)
        except:
            pass
        finally:
            sock.close()
        port_queue.task_done()

def save_results(filename, data):
    with open(filename, 'w') as f:
        f.write(data)

def main():
    target = input("Enter IP or domain: ").strip()
    ip = resolve_hostname(target)
    if not ip:
        print("Could not resolve hostname/IP.")
        return

    print(f"Host: {target}")
    print(f"Resolved IP: {ip}")

    dns_info = get_dns_info(target)
    if dns_info:
        print(f"DNS Info: {dns_info}")
    else:
        print("DNS info not available.")

    ip_info = get_ip_info(ip)
    if ip_info:
        print("IP info:\n-------------------")
        for key, value in ip_info.items():
            print(f"{key}: {value}")
    else:
        print("Failed to retrieve IP info.")

    whois_info = whois_lookup(target)
    if whois_info:
        print("WHOIS info:\n", whois_info)
    else:
        print("WHOIS lookup failed or no data available.")

    # Optional: Save output to a file
    save_choice = input("Save results to file? (y/n): ").strip().lower()
    if save_choice == 'y':
        filename = input("Enter filename: ").strip()
        data = f"Host: {target}\nResolved IP: {ip}\n"
        data += f"DNS Info: {dns_info}\n" if dns_info else "DNS Info: N/A\n"
        data += "IP info:\n"
        if ip_info:
            for key, value in ip_info.items():
                data += f"{key}: {value}\n"
        else:
            data += "Failed to retrieve IP info.\n"
        data += "WHOIS info:\n"
        if whois_info:
            data += str(whois_info) + "\n"
        else:
            data += "WHOIS lookup failed.\n"
        save_results(filename, data)
        print(f"Results saved to {filename}")

    # Port scanning
    print("Port scan (ports 1-1024):")
    port_queue = queue.Queue()
    open_ports = []

    for port in range(1, 1025):
        port_queue.put(port)

    threads = []
    for _ in range(100):
        t = threading.Thread(target=port_scan, args=(ip, port_queue, open_ports))
        t.start()
        threads.append(t)

    port_queue.join()

    for _ in range(100):
        port_queue.put(None)
    for t in threads:
        t.join()

    if open_ports:
        print("Open ports:", sorted(open_ports))
    else:
        print("No open ports found in 1-1024 range.")

if __name__ == "__main__":
    main()
