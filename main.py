import requests
import warnings
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from colorama import Fore
from pystyle import Center, Colors, Colorate
import os
import time


# Chromium Variables
chrome_path = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe' # Set to "" if you want to use the PATH variable instead
driver_path = 'chromedriver.exe' # Set to "" to use the PATH variable
twitch_username = "" # Enter your twitch username here


warnings.filterwarnings("ignore", category=DeprecationWarning)

BANNER = Colorate.Vertical(Colors.green_to_cyan, Center.XCenter("""           
       ▄█   ▄█▄  ▄█    ▄████████    ▄█    █▄     ▄█  
       ███ ▄███▀ ███   ███    ███   ███    ███   ███  
       ███▐██▀   ███▌  ███    █▀    ███    ███   ███▌ 
      ▄█████▀    ███▌  ███         ▄███▄▄▄▄███▄▄ ███▌ 
     ▀▀█████▄    ███▌  ███        ▀▀███▀▀▀▀███▀  ███▌ 
       ███▐██▄   ███   ███    █▄    ███    ███   ███  
       ███ ▀███▄ ███   ███    ███   ███    ███   ███  
       ███   ▀█▀ █▀    ████████▀    ███    █▀    █▀   
       ▀                                             
Improvements can be made to the code. If you're getting an error, visit my Discord.
                Discord: discord.gg/u4T67NU6xb    
                Github: github.com/kichi779  
"""))

def check_for_updates():
    """Check if a new version is available on GitHub."""
    try:
        r = requests.get("https://raw.githubusercontent.com/Kichi779/Twitch-Viewer-Bot/main/version.txt")
        remote_version = r.text.strip()
        
        with open('version.txt', 'r') as f:
            local_version = f.read().strip()
        
        if remote_version != local_version:
            print("A new version is available. Please download the latest version from GitHub.")
            time.sleep(3)
            return False
        return True
    except requests.RequestException:
        return True  # Ignore errors if unable to check for updates

def print_announcement():
    """Fetch and print announcements from GitHub."""
    try:
        r = requests.get("https://raw.githubusercontent.com/Kichi779/Twitch-Viewer-Bot/main/announcement.txt", headers={"Cache-Control": "no-cache"})
        return r.text.strip()
    except requests.RequestException:
        print("Could not retrieve announcement from GitHub.\n")
        return ""

def main():
    if not check_for_updates():
        return
    
    print(BANNER)

    announcement = print_announcement()
    print("\n", Colors.red, Center.XCenter("ANNOUNCEMENT"))
    print(Colors.yellow, Center.XCenter(f"{announcement}\n\n"))

    proxy_servers = {
        1: "https://www.blockaway.net",
        2: "https://www.croxyproxy.com",
        3: "https://www.croxyproxy.rocks",
        4: "https://www.croxy.network",
        5: "https://www.croxy.org",
        6: "https://www.youtubeunblocked.live",
        7: "https://www.croxyproxy.net",
    }

    # Set proxy server
    print(Colors.green, "Proxy Server 1 Is Recommended")
    print(Colorate.Vertical(Colors.green_to_blue, "Please select a proxy server (1,2,3..):"))
    for i in range(1, 8):
        print(Colorate.Vertical(Colors.red_to_blue, f"Proxy Server {i}"))
    try:
        proxy_choice = int(input("> "))
        proxy_url = proxy_servers.get(proxy_choice, proxy_servers[1])  # Default to Proxy 1 if invalid
    except ValueError:
        print("Invalid choice. Using default proxy (1).")
        proxy_url = proxy_servers[1]


    # Set proxy server
    if not twitch_username:
        twitch_username = input(Colorate.Vertical(Colors.green_to_blue, "Enter your channel name (e.g Kichi779): "))


    # Set proxy count
    try:
        proxy_count = int(input(Colorate.Vertical(Colors.cyan_to_blue, "How many proxy sites do you want to open? (Viewers to send): ")))
    except ValueError:
        print("Invalid input. Defaulting to 1 viewer.")
        proxy_count = 1
    os.system("cls" if os.name == "nt" else "clear")


    # Configure Chrome options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_argument('--disable-logging')
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument("--mute-audio")
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = None


    # AdBlock Extension
    extension_path = 'adblock.crx'
    chrome_options.add_extension(extension_path)


    # Set Chrome binary path if defined
    if chrome_path:
        chrome_options.binary_location = chrome_path


    # Initialize WebDriver with driver_path if defined
    if driver_path:
        driver = webdriver.Chrome(executable_path=driver_path, options=chrome_options)
    else:
        driver = webdriver.Chrome(options=chrome_options)

    driver.get(proxy_url)


    # Initializing viewers
    print(BANNER)
    print(Colors.red, "Initializing viewers... Please wait a few minutes... Do not close this window.")
    print(Colors.red, "If the viewers do not arrive, restart the program with Cmd-Q or Ctrl-Q and try again.")
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(proxy_url)

        for _ in range(proxy_count):
            driver.execute_script("window.open('" + proxy_url + "')")
            driver.switch_to.window(driver.window_handles[-1])
            driver.get(proxy_url)

            text_box = driver.find_element(By.ID, 'url')
            text_box.send_keys(f'www.twitch.tv/{twitch_username}')
            text_box.send_keys(Keys.RETURN)
        
        input(Colorate.Vertical(Colors.red_to_blue, "Finished initializing viewers. Keep this window open to keep them alive.")
        input(Colorate.Vertical(Colors.red_to_blue, "If you want to stop them, close this program with Cmd-Q or Ctrl-Q")

        # Refresh tabs every 3 minutes
        while True:
            time.sleep(180)  # Wait for 3 minutes
            for handle in driver.window_handles:
                driver.switch_to.window(handle)
                driver.refresh()

    finally:
        if driver:
            driver.quit()

if __name__ == '__main__':
    main()
