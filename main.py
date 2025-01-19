import requests
import warnings
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

def save_settings(twitch_username, set_160p):
    with open('settings.txt', 'w') as file:
        file.write(f"Twitch Username: {twitch_username}\n")
        file.write(f"Set 160p: {set_160p}\n")

def load_settings():
    try:
        with open('settings.txt', 'r') as file:
            lines = file.readlines()
            if len(lines) >= 2:
                twitch_username = lines[0].split(': ')[1].strip()
                set_160p = lines[1].split(': ')[1].strip()
                return twitch_username, set_160p
    except:
        pass
    return None, None

def set_stream_quality(driver):
    wait = WebDriverWait(driver, 15)
    
    element_video = None
    while not element_video:
        try:
            # Ad
            element_video_ad_xpath = "//div[@data-test-selector='sad-overlay']"
            element_video = driver.find_element(By.XPATH, element_video_ad_xpath)
        except:
            # No ad
            element_video_xpath = "//div[@data-a-target='player-overlay-click-handler']"
            element_video = driver.find_element(By.XPATH, element_video_xpath)
        time.sleep(0.5)
        
    actions = ActionChains(driver)

    actions.move_to_element(element_video).perform()

    settings_button = driver.find_element(By.XPATH, "//button[@aria-label='Settings']")
    settings_button.click()

    quality_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Quality']")))
    quality_option.click()

    quality_levels_parent = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@data-a-target='player-settings-menu']")))
    quality_levels = quality_levels_parent.find_elements(By.XPATH, './*')
    
    last_btn = quality_levels[len(quality_levels)-1]
    last_btn.click()  # Last button because sometimes 160p is not available

def print_announcement():
    try:
        r = requests.get("https://raw.githubusercontent.com/Kichi779/Twitch-Viewer-Bot/main/announcement.txt", headers={"Cache-Control": "no-cache"})
        announcement = r.content.decode('utf-8').strip()
        return announcement
    except:
        print("Could not retrieve announcement from GitHub.\n")

def reopen_pages(driver, proxy_url, twitch_username, proxy_count):
    """Funzione per chiudere e riaprire periodicamente le pagine proxy."""
    while True:
        print(Colors.yellow, Center.XCenter("Chiudendo e riaprendo le pagine proxy..."))

        # Chiude tutte le finestre tranne la prima
        while len(driver.window_handles) > 1:
            driver.switch_to.window(driver.window_handles[-1])
            driver.close()

        # Riapre le finestre richieste
        driver.switch_to.window(driver.window_handles[0])
        for i in range(proxy_count):
            try:
                driver.execute_script("window.open('" + proxy_url + "')")  # Apri una nuova scheda vuota
                driver.switch_to.window(driver.window_handles[-1])  # Passa alla nuova scheda
                driver.get(proxy_url)  # Carica l'URL del proxy nella nuova scheda

                # Attendi che il campo di input 'url' sia presente e interagibile
                text_box = driver.find_element(By.ID, 'url')
                text_box.send_keys(f'www.twitch.tv/{twitch_username}')
                text_box.send_keys(Keys.RETURN)
            except Exception as e:
                print(f"Errore durante l'apertura di una nuova scheda: {e}")
        
        time.sleep(60)  # Attendi 60 secondi prima di riaprire

def main():
    if not check_for_updates():
        return

    twitch_username, set_160p = load_settings()

    os.system(f"title Kichi779 - Twitch Viewer Bot @kichi#0779 ")

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

    # Selecting proxy server
    print(Colors.green,"Proxy Server 1 Is Recommended")
    print(Colorate.Vertical(Colors.green_to_blue,"Please select a proxy server(1,2,3..):"))
    for i in range(1, 7):
        print(Colorate.Vertical(Colors.red_to_blue,f"Proxy Server {i}"))
    proxy_choice = int(input("> "))
    proxy_url = proxy_servers.get(proxy_choice)

    if not proxy_url:
        print("Invalid proxy server selection.")
        return

    twitch_username = twitch_username or input(Colorate.Vertical(Colors.green_to_blue, "Enter your channel name (e.g Kichi779): "))
    set_160p = set_160p or input(Colorate.Vertical(Colors.purple_to_red,"Do you want to set the stream quality to 160p? (yes/no): "))
    save_settings(twitch_username, set_160p)

    proxy_count = int(input(Colorate.Vertical(Colors.cyan_to_blue, "How many proxy sites do you want to open? (Viewer to send)")))
    os.system("cls")

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
                             Discord discord.gg/u4T67NU6xb    
                             Github  github.com/kichi779    """)))
    print('')
    print('')
    print(Colors.red, Center.XCenter("Viewers Send. Please don't hurry. If the viewers does not arrive, turn it off and on and do the same operations"))

    chrome_path = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
    driver_path = 'chromedriver.exe'

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_argument('--disable-logging')
    chrome_options.add_argument('--log-level=3')
    # Rimuovi '--headless' per il debugging
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--mute-audio")
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    # Disabilita temporaneamente Adblock per debugging
    # extension_path = 'adblock.crx'
    # chrome_options.add_extension(extension_path)
    
    driver = webdriver.Chrome(options=chrome_options)

    # Apri le pagine iniziali
    driver.get(proxy_url)
    for i in range(proxy_count):
        try:
            driver.execute_script("window.open('" + proxy_url + "')")  # Apri una nuova scheda vuota
            driver.switch_to.window(driver.window_handles[-1])  # Passa alla nuova scheda
            driver.get(proxy_url)  # Carica l'URL del proxy nella nuova scheda

            # Attendi che il campo di input 'url' sia presente e interagibile
            text_box = driver.find_element(By.ID, 'url')
            text_box.send_keys(f'www.twitch.tv/{twitch_username}')
            text_box.send_keys(Keys.RETURN)
        except Exception as e:
            print(f"Errore durante l'apertura di una nuova scheda: {e}")
    
    if set_160p.lower() == 'yes':
        set_stream_quality(driver)

    # Riavvio periodico delle pagine
    reopen_pages(driver, proxy_url, twitch_username, proxy_count)

if __name__ == "__main__":
    main()
