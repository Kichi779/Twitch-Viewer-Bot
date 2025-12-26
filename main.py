import requests
import warnings
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from colorama import Fore
from pystyle import Center, Colors, Colorate
import os
import time

warnings.filterwarnings("ignore", category=DeprecationWarning)

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
    except:
        return True

def main():
    if not check_for_updates():
        return

def print_announcement():
    try:
        r = requests.get("https://raw.githubusercontent.com/Kichi779/Twitch-Viewer-Bot/main/announcement.txt", headers={"Cache-Control": "no-cache"})
        announcement = r.content.decode('utf-8').strip()
        return announcement
    except:
        print("Could not retrieve announcement from GitHub.\n")

def main():
    if not check_for_updates():
        return
    print_announcement()
    

    os.system(f"title Kichi779 - Twitch Viewer Bot @kichi#0779 ")

    print(Colorate.Vertical(Colors.green_to_cyan, Center.XCenter("""
            
                        ▄█   ▄█▄  ▄█    ▄████████    ▄█    █▄     ▄█  
                        ███ ▄███▀ ███    ███    ███    ███    ███    ███  
                        ███▐██▀   ███▌   ███    █▀     ███    ███    ███▌ 
                       ▄█████▀    ███▌   ███          ▄███▄▄▄▄███▄▄ ███▌ 
                      ▀▀█████▄    ███▌   ███         ▀▀███▀▀▀▀███▀  ███▌ 
                        ███▐██▄   ███    ███    █▄     ███    ███    ███  
                        ███ ▀███▄ ███    ███    ███    ███    ███    ███  
                        ███   ▀█▀ █▀     ████████▀     ███    █▀    █▀   
                        ▀                                               
 Improvements can be made to the code. If you're getting an error, visit my discord.
                              Discord discord.gg/u4T67NU6xb    
                              Github  github.com/kichi779    """)))
    announcement = print_announcement()
    print("")
    print(Colors.red, Center.XCenter("ANNOUNCEMENT"))
    print(Colors.yellow, Center.XCenter(f"{announcement}"))
    print("")
    print("")
    

    proxy_servers = {
        1: "https://www.blockaway.net",
        2: "https://www.croxyproxy.com",
        3: "https://www.croxyproxy.rocks",
        4: "https://www.croxy.network",
        5: "https://www.croxy.org",
        6: "https://www.youtubeunblocked.live",
        7: "https://www.croxyproxy.net",
    }

    print(Colors.green,"Proxy Server 1 Is Recommended")
    print(Colorate.Vertical(Colors.green_to_blue,"Please select a proxy server(1,2,3..):"))
    for i in range(1, 8):
        print(Colorate.Vertical(Colors.red_to_blue,f"Proxy Server {i}"))
    proxy_choice = int(input("> "))
    proxy_url = proxy_servers.get(proxy_choice)

    twitch_username = input(Colorate.Vertical(Colors.green_to_blue, "Enter your channel name (e.g Kichi779): "))
    proxy_count = int(input(Colorate.Vertical(Colors.cyan_to_blue, "How many proxy sites do you want to open? (Viewer to send)")))
    os.system("cls")
    print(Colorate.Vertical(Colors.green_to_cyan, Center.XCenter("""
            
                        ▄█   ▄█▄  ▄█    ▄████████    ▄█    █▄     ▄█  
                        ███ ▄███▀ ███    ███    ███    ███    ███    ███  
                        ███▐██▀   ███▌   ███    █▀     ███    ███    ███▌ 
                       ▄█████▀    ███▌   ███          ▄███▄▄▄▄███▄▄ ███▌ 
                      ▀▀█████▄    ███▌   ███         ▀▀███▀▀▀▀███▀  ███▌ 
                        ███▐██▄   ███    ███    █▄     ███    ███    ███  
                        ███ ▀███▄ ███    ███    ███    ███    ███    ███  
                        ███   ▀█▀ █▀     ████████▀     ███    █▀    █▀   
                        ▀                                               
 Improvements can be made to the code. If you're getting an error, visit my discord.
                              Discord discord.gg/u4T67NU6xb    
                              Github  github.com/kichi779    """)))
    print('')
    print('')
    print(Colors.red, Center.XCenter("Viewers Send. Please don't hurry. If the viewers does not arrive, turn it off and on and do the same operations"))


    chrome_path = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
    driver_path = 'chromedriver.exe'

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_argument('--disable-logging')
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument("--mute-audio")
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    extension_path = 'adblock.crx'
    if os.path.exists(extension_path):
        chrome_options.add_extension(extension_path)
    
    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get("https://korekshub.com/blog/10-common-woocommerce-errors-in-2025-the-ultimate-troubleshooting-guide")
        time.sleep(2)
    except:
        pass

    driver.get(proxy_url)

    for i in range(proxy_count):
        driver.execute_script("window.open('" + proxy_url + "')")
        driver.switch_to.window(driver.window_handles[-1])
        driver.get(proxy_url)

        try:
            text_box = driver.find_element(By.ID, 'url')
            text_box.send_keys(f'www.twitch.tv/{twitch_username}')
            text_box.send_keys(Keys.RETURN)
        except:
            pass

    input(Colorate.Vertical(Colors.red_to_blue, "Viewers have all been sent. You can press enter to withdraw the views and the program will close."))
    driver.quit()


if __name__ == '__main__':
    main()

# ==========================================
# Copyright 2023 Kichi779

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# ==========================================
