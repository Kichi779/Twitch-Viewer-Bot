# -*- coding: utf-8 -*-

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
        # Link al file della versione remota
        version_url = "https://pastebin.com/raw/asYWrVC0"
        remote_version = requests.get(version_url).content.decode('utf-8').strip()
        
        # Lettura della versione locale
        local_version_path = 'version.txt'
        if not os.path.exists(local_version_path):
            # Se il file locale non esiste, crearlo con una versione predefinita
            with open(local_version_path, 'w') as f:
                f.write("0.0.0")
        local_version = open(local_version_path, 'r').read().strip()
        
        if remote_version != local_version:
            print(f"Una nuova versione ({remote_version}) è disponibile.")
            user_choice = input("Vuoi scaricare l'aggiornamento? (s/n): ").strip().lower()
            if user_choice == 's':
                # Link ai file aggiornati
                main_file_url = "https://www.dropbox.com/scl/fi/xhqc0089qg703mw4sr25t/main.py?rlkey=bwh2gwx2f2z1xp0i6easxc8vq&st=sp5t6u32&dl=1"  # URL al file main.py
                version_file_url = "https://pastebin.com/raw/asYWrVC0"  # URL al file version.txt

                try:
                    # Scarica e salva main.py
                    print("Scaricamento di main.py...")
                    main_content = requests.get(main_file_url).content.decode('utf-8')
                    with open('main.py', 'w') as main_file:
                        main_file.write(main_content)

                    # Scarica e salva version.txt
                    print("Scaricamento di version.txt...")
                    version_content = requests.get(version_file_url).content.decode('utf-8')
                    with open('version.txt', 'w') as version_file:
                        version_file.write(version_content)

                    print("Aggiornamento completato con successo!")
                    time.sleep(5)
                    os.system("cls")
                except Exception as e:
                    print(f"Errore durante il download dei file: {e}")
                return False
            else:
                print("Aggiornamento annullato.")
                return False
        else:
            print("Il programma è già aggiornato.")
            return True
    except Exception as e:
        print(f"Errore durante il controllo degli aggiornamenti: {e}")
        return True

def save_settings(twitch_username):
    with open('settings.txt', 'w') as file:
        file.write(f"Twitch Username: {twitch_username}\n")
        #file.write(f"Set 160p: {set_160p}\n")    

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
    last_btn.click()  # Last btn because sometimes 160p not available

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
            driver.execute_script("window.open('')")  # Open a new empty window
            new_window_handle = driver.window_handles[-1]  # Get the handle of the newly opened window
            driver.switch_to.window(new_window_handle)
            driver.get(proxy_url)

            time.sleep(2)  # Aggiungi un ritardo per il caricamento della pagina

            text_box = driver.find_element(By.ID, 'url')
            text_box.send_keys(f'www.twitch.tv/{twitch_username}')
            text_box.send_keys(Keys.RETURN)

        time.sleep(60)  # Attendi 60 secondi prima di riaprire

def main():
    if not check_for_updates():
        return

    twitch_username = load_settings()

    os.system(f"title xLamday - Twitch Viewer Bot @xLamday ")

    print(Colorate.Vertical(Colors.green_to_cyan, Center.XCenter("""
           

                    __                          __             
             _  __ / /   ____ _ ____ ___   ____/ /____ _ __  __
            | |/_// /   / __ `// __ `__ \ / __  // __ `// / / /
            _>  < / /___/ /_/ // / / / / // /_/ // /_/ // /_/ / 
            /_/|_|/_____/\__,_//_/ /_/ /_/ \__,_/ \__,_/ \__, /  
                                                        /____/   

 E' possibile fare migliorie al codice. Se riscontri un errore, visita il mio discord.
                             Discord discord.gg/yzreKA4xZD   
                             Github  github.com/xLamday    """)))

    # announcement = print_announcement()
    # print("")
    # print(Colors.red, Center.XCenter("ANNOUNCEMENT"))
    # print(Colors.yellow, Center.XCenter(f"{announcement}"))
    # print("")
    # print("")

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
    print(Colors.green, "Proxy Server 1 è raccomandato")
    print(Colorate.Vertical(Colors.green_to_blue, "Seleziona un proxy server (1,2,3..):"))
    for i in range(1, 7):
        print(Colorate.Vertical(Colors.red_to_blue, f"Proxy Server {i}"))
    proxy_choice = int(input("> "))
    proxy_url = proxy_servers.get(proxy_choice)

    if twitch_username is None:
        twitch_username = input(Colorate.Vertical(Colors.green_to_blue, "Inserisci il nome del canale (e.g xlamday): "))
        #set_160p = input(Colorate.Vertical(Colors.purple_to_red, "Do you want to set the stream quality to 160p? (yes/no): "))
        save_settings(twitch_username)
    else:
        use_settings = input(Colorate.Vertical(Colors.green_to_blue, "Vuoi utilizzare le tue impostazioni salvate? (si/no): "))
        if use_settings.lower() == "no":
            twitch_username = input(Colorate.Vertical(Colors.green_to_blue, "Inserisci il nome del canale (e.g xlamday): "))
            #set_160p = input(Colorate.Vertical(Colors.purple_to_red, "Do you want to set the stream quality to 160p? (yes/no): "))
            save_settings(twitch_username)

    proxy_count = int(input(Colorate.Vertical(Colors.cyan_to_blue, "Quanti spettatori vuoi inviare? ")))
    os.system("cls")
    print(Colorate.Vertical(Colors.green_to_cyan, Center.XCenter("""

                        __                          __             
                _  __ / /   ____ _ ____ ___   ____/ /____ _ __  __
                | |/_// /   / __ `// __ `__ \ / __  // __ `// / / /
                _>  < / /___/ /_/ // / / / / // /_/ // /_/ // /_/ / 
                /_/|_|/_____/\__,_//_/ /_/ /_/ \__,_/ \__,_/ \__, /  
                                                            /____/   

 E' possibile fare migliorie al codice. Se riscontri un errore, visita il mio discord.
                             Discord discord.gg/yzreKA4xZD    
                             Github  github.com/xLamday    """)))
    print('')
    print('')
    print(Colors.red, Center.XCenter("Spettatori in invio. Non avere fretta. Se gli spettatori non dovessero funzionare correttamente, prova a riavviare il programma e rifare le operazioni."))

    chrome_path = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
    driver_path = 'chromedriver.exe'

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_argument('--disable-logging')
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument("--mute-audio")
    chrome_options.add_argument('--disable-dev-shm-usage')
    # ADBLOCK EXT
    extension_path = 'adblock.crx'
    chrome_options.add_extension(extension_path)
    driver = webdriver.Chrome(options=chrome_options)

    # pagine iniziali
    driver.get(proxy_url)
    for i in range(proxy_count):
        driver.switch_to.new_window('tab')
        driver.get(proxy_url)

        time.sleep(0.3)  # ritardo per il caricamento della pagina

        text_box = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, 'url'))
        )
        text_box.send_keys(f'www.twitch.tv/{twitch_username}')
        text_box.send_keys(Keys.RETURN)

    # Riapri periodicamente le pagine
    reopen_pages(driver, proxy_url, twitch_username, proxy_count)

if __name__ == '__main__':
    main()
