import os
import warnings
import requests
import random
import logging
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from colorama import Fore
from pystyle import Center, Colors, Colorate
import time

warnings.filterwarnings("ignore", category=DeprecationWarning)

# Disable logging from selenium
logging.getLogger('WDM').setLevel(logging.NOTSET)

# Function to check for updates from GitHub
def check_for_updates():
    try:
        r = requests.get("https://raw.githubusercontent.com/Kichi779/Twitch-Viewer-Bot/main/version.txt")
        remote_version = r.content.decode('utf-8').strip()
        local_version = open('version.txt', 'r').read().strip()
        if remote_version != local_version:
            print("A new version is available. Please download the latest version from GitHub.")
            time.sleep(3)
            return False
        return True
    except Exception as e:
        log_error(f"Failed to check for updates: {str(e)}")
        return True

# Function to save user settings to settings.txt
def save_settings(twitch_username):
    with open('settings.txt', 'w') as file:
        file.write(f"Twitch Username: {twitch_username}\n")

# Function to load user settings from settings.txt
def load_settings():
    try:
        with open('settings.txt', 'r') as file:
            lines = file.readlines()
            if len(lines) >= 1:
                twitch_username = lines[0].split(': ')[1].strip()
                return twitch_username
    except Exception as e:
        log_error(f"Failed to load settings: {str(e)}")
    return None

# Function to print announcement from announcement.txt
def print_announcement():
    try:
        r = requests.get("https://raw.githubusercontent.com/Kichi779/Twitch-Viewer-Bot/main/announcement.txt", headers={"Cache-Control": "no-cache"})
        announcement = r.content.decode('utf-8').strip()
        return announcement
    except Exception as e:
        log_error(f"Failed to retrieve announcement: {str(e)}")
        print("Could not retrieve announcement from GitHub.\n")

# Function to get terminal size
def get_terminal_size():
    try:
        rows, columns = os.popen('stty size', 'r').read().split()
        return int(rows), int(columns)
    except Exception as e:
        log_error(f"Failed to get terminal size: {str(e)}")
        return 24, 80

# Function to log errors to error_log.txt
def log_error(message):
    try:
        with open('error_log.txt', 'a') as file:
            file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} ERROR: {message}\n")
    except Exception as e:
        print(f"Failed to log error: {str(e)}")

# Main function
def main():
    try:
        if not check_for_updates():
            return

        announcement = print_announcement()
        print("")
        print(Colors.red, Center.XCenter("ANNOUNCEMENT"))
        print(Colors.yellow, Center.XCenter(f"{announcement}"))
        print("")
        print("")

        proxy_servers = ['https://www.blockaway.net', 'https://www.croxyproxy.com', 'https://www.croxyproxy.rocks', 'https://www.croxy.network', 'https://www.croxy.org', 'https://www.youtubeunblocked.live', 'https://www.croxyproxy.net']

        def selectRandom(proxy_servers):
            return random.choice(proxy_servers)

        proxy_url = selectRandom(proxy_servers)

        print(Colors.red, "Proxy servers are randomly selected every time")
        twitch_username = load_settings()

        if twitch_username is None:
            twitch_username = input(Colorate.Vertical(Colors.green_to_blue, "Enter your channel name (e.g Kichi779): "))
            save_settings(twitch_username)
        else:
            use_settings = input(Colorate.Vertical(Colors.green_to_blue, "Do you want to use your saved settings? (yes/no): "))
            if use_settings.lower() == "no":
                twitch_username = input(Colorate.Vertical(Colors.green_to_blue, "Enter your channel name (e.g Kichi779): "))
                save_settings(twitch_username)

        proxy_count = int(input(Colorate.Vertical(Colors.cyan_to_blue, "How many proxy sites do you want to open? (Viewer to send)")))

        os.system("cls")
        try:
            print(Colorate.Vertical(Colors.green_to_cyan, Center.XCenter("""
           
                       ▄█   ▄█▄  ▄█    ▄████████    ▄█    █▄     ▄█  
                       ███ ▄███▀ ███   ███    ███   ███    ███   ███  
                       ███▐██▀   ███▌  ███    █▀    ███    ███   ███▌ 
                      ▄█████▀    ███▌  ███         ▄███▄▄▄▄███▄▄ ███▌ 
                     ▀▀█████▄    ███▌  ███        ▀▀███▀▀▀▀███▀  ███▌ 
                       ███▐██▄   ███   ███    █▄    ███    ███   ███  
                       ███ ▀███▄ ███   ███    ███   ███    ███   ███  
                       ███   ▀█▀ █▀    ████████▀    ███    █▀    █▀   
                       ▀                                             
 Improvements can be made to the code. If you're getting an error, visit my discord.
                             Discord discord.gg/UkSJP8RUxc    
                             Github  github.com/kichi779    """)))
        except ValueError:
            rows, columns = get_terminal_size()
            print("\n".join([" " * ((columns - len(line)) // 2) + line for line in """
           
                       ▄█   ▄█▄  ▄█    ▄████████    ▄█    █▄     ▄█  
                       ███ ▄███▀ ███   ███    ███   ███    ███   ███  
                       ███▐██▀   ███▌  ███    █▀    ███    ███   ███▌ 
                      ▄█████▀    ███▌  ███         ▄███▄▄▄▄███▄▄ ███▌ 
                     ▀▀█████▄    ███▌  ███        ▀▀███▀▀▀▀███▀  ███▌ 
                       ███▐██▄   ███   ███    █▄    ███    ███   ███  
                       ███ ▀███▄ ███   ███    ███   ███    ███   ███  
                       ███   ▀█▀ █▀    ████████▀    ███    █▀    █▀   
                       ▀                                             
 Improvements can be made to the code. If you're getting an error, visit my discord.
                             Discord discord.gg/UkSJP8RUxc    
                             Github  github.com/kichi779    """.splitlines()]))

        chrome_path = "C:\Program Files\Google\Chrome\Application\chrome.exe"
        for i in range(proxy_count):
            proxy_url = selectRandom(proxy_servers)

            chrome_options = webdriver.ChromeOptions()
            chrome_options.binary_location = chrome_path
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--mute-audio')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--disable-software-rasterizer')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_argument('--disable-background-networking')
            chrome_options.add_argument('--disable-background-timer-throttling')
            chrome_options.add_argument('--disable-backgrounding-occluded-windows')
            chrome_options.add_argument('--disable-breakpad')
            chrome_options.add_argument('--disable-client-side-phishing-detection')
            chrome_options.add_argument('--disable-component-update')
            chrome_options.add_argument('--disable-default-apps')
            chrome_options.add_argument('--disable-extensions')
            chrome_options.add_argument('--disable-features=TranslateUI')
            chrome_options.add_argument('--disable-hang-monitor')
            chrome_options.add_argument('--disable-ipc-flooding-protection')
            chrome_options.add_argument('--disable-popup-blocking')
            chrome_options.add_argument('--disable-prompt-on-repost')
            chrome_options.add_argument('--disable-renderer-backgrounding')
            chrome_options.add_argument('--disable-sync')
            chrome_options.add_argument('--disable-web-resources')
            chrome_options.add_argument('--enable-automation')
            chrome_options.add_argument('--force-fieldtrials=*BackgroundTracing/default/')
            chrome_options.add_argument('--force-renderer-accessibility')
            chrome_options.add_argument('--ignore-certificate-errors')
            chrome_options.add_argument('--metrics-recording-only')
            chrome_options.add_argument('--no-first-run')
            chrome_options.add_argument('--password-store=basic')
            chrome_options.add_argument('--use-mock-keychain')

            chrome_options.add_argument('--log-level=3')
            chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

            driver = webdriver.Chrome(options=chrome_options)
            driver.get(proxy_url)

            search_box = driver.find_element(By.NAME, "q")
            search_box.send_keys(f"https://www.twitch.tv/{twitch_username}")
            search_box.send_keys(Keys.RETURN)

            print(f"Proxy {i+1}: {proxy_url}")

        print("All proxies have been opened.")

    except Exception as e:
        log_error(f"Unexpected error: {str(e)}")
        print("An unexpected error occurred. Please check error_log.txt for details.")

if __name__ == "__main__":
    main()
