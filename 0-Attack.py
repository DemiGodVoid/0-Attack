import os
import time
RED = "\033[31m"
GREEN = "\033[32m"
BLUE = "\033[34m"
RESET = "\033[0m"
os.system('clear')
print(f"{RED} 0-Attack {RESET}")
time.sleep(1)
print(f"""{RED}

   ███___ ___    _____  _________  ____  __.  _________      
   ███░/   |   \  /  _  \ \_   ___ \|    |/ _| /   _____/      
 ███░ /    ~    \/  /_\  \/    \  \/|      <   \_____  \       
██░   \    Y    /    |    \     \___|    |  \  /        \      
░      \___|_  /\____|__  /\______  /____|__ \/_______  /    
           ██\/         \/    ░   \/        \/░       \/{RESET}

  




{GREEN}Multi-Tool                        Coded: Nihility
--------------------------------------------------------
1. DDoS Attack                        2. Web Scanner
    
3. File Fuckery(windows)              4. Network Scan

5. IP-Lookup                          6. Android RAT


--------------------------------------------------------{RESET}
      """)
choice = input(f"{BLUE}Choose an option: {RESET}")
if choice == "1":
    os.system("python tools/ddos.py")

elif choice == "2":
    os.system("python tools/wscan.py")

elif choice == "3":
    os.system("python tools/file_Fuckery.py")

elif choice == "4":
    os.system("python tools/network_scan.py")

elif choice == "5":
    os.system("python tools/IpLookup.py")

elif choice == "6":
    os.system("python tools/ar.py")
