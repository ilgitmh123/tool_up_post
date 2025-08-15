import os
import time
import random
import pyperclip
import win32clipboard
from PIL import Image
import io
import pyautogui
import schedule
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
cookie = "" #Dán cookie fb các bác vào đây
def get_chrome_driver():
    options = webdriver.ChromeOptions()
    options.debugger_address = "127.0.0.1:9995"
    driver = webdriver.Chrome(options=options)
    return driver
def maintain_fb(cookie_value,driver):
    driver.get("https://www.facebook.com")
    script = f"""
    javascript:void(function(){{
        function setCookie(t){{
            var list=t.split(';');
            console.log(list);
            for(var i=list.length-1;i>=0;i--) {{
                var cname=list[i].split('=')[0];
                var cvalue=list[i].split('=')[1];
                var d=new Date();
                d.setTime(d.getTime()+(7*24*60*60*1000));  
                var expires=';domain=.facebook.com;expires='+d.toUTCString();
                document.cookie=cname+'='+cvalue+'; '+expires;
            }}
        }}
        function hex2a(hex){{
            var str='';
            for(var i=0;i<hex.length;i+=2){{
                var v=parseInt(hex.substr(i,2),16);
                if(v)str+=String.fromCharCode(v);
            }}
            return str;
        }}
        setCookie('{cookie_value}');  // Cập nhật cookie
        location.href='https://facebook.com';  // Chuyển hướng đến Facebook
    }})()
    """
    driver.execute_script(script)
def copy_text(text):
    pyperclip.copy(text)
    time.sleep(0.3)

def copy_image(image_path):
    image = Image.open(image_path)
    output = io.BytesIO()
    image.convert("RGB").save(output, "BMP")
    data = output.getvalue()[14:]
    output.close()

    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
    win32clipboard.CloseClipboard()
    time.sleep(0.3)

def copy_content_and_images(content_file, image_folder):
    with open(content_file, "r", encoding="utf-8") as f:
        content_text = f.read().strip()

    copy_text(content_text)
    pyautogui.hotkey("ctrl", "v")  
    time.sleep(1)
    for file_name in sorted(os.listdir(image_folder)):
        if file_name.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif")):
            img_path = os.path.join(image_folder, file_name)
            copy_image(img_path)
            pyautogui.hotkey("ctrl", "v")  # Dán ảnh
            time.sleep(1.5)  # Chờ ảnh load

def dang(driver):
    element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//span[contains(text(),'Bạn viết gì đi')]"))
    )
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", element)
    time.sleep(random.uniform(0.4, 0.8))
    size = element.size
    width = max(int(size['width']), 6)
    height = max(int(size['height']), 6)
    offset_x = random.randint(1, width - 1)
    offset_y = random.randint(1, height - 1)

    try:
        actions = ActionChains(driver)
        actions.move_to_element_with_offset(element, offset_x, offset_y)
        actions.pause(random.uniform(0.2, 0.5))
        actions.click()
        actions.perform()
    except:
        element.click()
    time.sleep(random.uniform(0.3, 0.7))

def click_up(driver):
    selector = "div[aria-label='Đăng'][role='button']"
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
    )
    ActionChains(driver).move_to_element(element).pause(0.2).click().perform()
    time.sleep(1)

def run_post_sequence(links, content_file, image_folder):
    driver = get_chrome_driver()
    driver.get("https://facebook.com")
    maintain_fb(cookie,driver)
    for link in links:
        driver.get(link)
        time.sleep(3)
        dang(driver)
        copy_content_and_images(content_file, image_folder)
        click_up(driver)
        time.sleep(5) 
links_list = [
    "https://www.facebook.com/groups/tuyendungforexcoin"
] 
# Link nhóm các bác muốn đăng bài vào đây
content_file_path = "content.txt"
image_folder_path = "images_folder"

#Đăng bài lúc mấy giờ nè ví dụ 16:13
schedule.every().day.at("16:13").do(
    run_post_sequence, links_list, content_file_path, image_folder_path
)
while True:
    schedule.run_pending()
    time.sleep(1)