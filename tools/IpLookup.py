# Ip lookup tool, kinda useless
import requests
IP = "127.0.0.1"

print("""NAME: Ip Lookup


Useless tool unless its for finding open ports
""")
print("EX: " + IP)
input = "IP: "
print("Finding results for " + input)
def ip_lookup(ip):

    response = requests.get(f"https://ipinfo.io/{ip}/json")
    if response.status_code == 200:
        data = response.json()
        print(f"{ip} info\n-------------------")
        for key, value in data.items():
            print(f"{key}: {value}")
    else:
        print("Failed to retrieve IP information.")

ip_lookup(input)
