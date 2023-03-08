from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from colorama import Fore
from pystyle import Center, Colors, Colorate
import os

os.system(f"title Kichi779 - Twitch Viewer Bot @kichi#4622 ")

print(Colorate.Vertical(Colors.blue_to_purple, Center.XCenter("""
           
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
                                       Discord https://discord.gg/aVk4JUFukk       
                                       Github  https://github.com/kichi779          
                       
                      
                      """)))


# Chrome location
chrome_path = 'D:\Program Files\Google\Chrome\Application\chrome.exe'
# The driver that has the same version as your currently installed Google chrome must be installed.
driver_path = 'chromedriver.exe'

twitch_username = input("Enter your channel name (e.g Kichi779): ")
proxy_count = int(input("How many proxy sites do you want to open? (Viewer to send)"))

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-logging')
chrome_options.add_argument('--log-level=3')
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.binary_location = chrome_path
driver = webdriver.Chrome(executable_path=driver_path, chrome_options=chrome_options)




driver.get('https://www.blockaway.net/')

text_box = driver.find_element(By.ID, 'url')
text_box.send_keys(f'www.twitch.tv/{twitch_username}')


text_box.send_keys(Keys.RETURN)

for i in range(proxy_count):
    driver.execute_script("window.open('https://www.blockaway.net/')")
    driver.switch_to.window(driver.window_handles[-1])
    text_box = driver.find_element(By.ID, 'url')
    text_box.send_keys(f'www.twitch.tv/{twitch_username}')
    text_box.send_keys(Keys.RETURN)


input("The specified proxy site has been opened. Please do not click the X button on the top right, press a button to close the sites...")

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
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ==========================================