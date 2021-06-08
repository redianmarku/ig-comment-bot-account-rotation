import time
import json
import random
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager as CM
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.utils import download_file
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


f = open('accounts.json',)
datas = json.load(f)

with open('tags.txt', 'r') as f:
    tags = [line.strip() for line in f]


def doesnt_exist(driver, xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return True
    else:
        return False


def random_comment():
    with open('comments.txt', 'r') as f:
        comments = [line.strip() for line in f]
    comment = random.choice(comments)
    return comment


def main(data):
    options = webdriver.ChromeOptions()

    mobile_emulation = {
        "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/90.0.1025.166 Mobile Safari/535.19"}

    options.add_experimental_option("mobileEmulation", mobile_emulation)
    options.add_argument("--log-level=3")

    bot = webdriver.Chrome(options=options, executable_path=CM().install())
    bot.set_window_size(500, 950)

    bot.get('https://instagram.com')

    # Login section==========================
    time.sleep(3)
    print('Logging in...')
    bot.find_element_by_xpath(
        '//*[@id="react-root"]/section/main/article/div/div/div/div[3]/button[1]').click()
    time.sleep(2)

    username_field = bot.find_element_by_xpath(
        '//*[@id="loginForm"]/div[1]/div[3]/div/label/input')
    username_field.send_keys(data["username"])

    time.sleep(1)

    password_field = bot.find_element_by_xpath(
        '//*[@id="loginForm"]/div[1]/div[4]/div/label/input')
    password_field.send_keys(data["password"])

    time.sleep(1)

    bot.find_element_by_xpath(
        '//*[@id="loginForm"]/div[1]/div[6]/button').click()

    time.sleep(6)
    # ==========================================

    # Fetching posts============================

    tag = random.choice(tags)
    print('Fetching posts for this tag----> ' + tag)
    link = "https://www.instagram.com/explore/tags/" + tag

    bot.get(link)
    time.sleep(4)

    for i in range(1):
        ActionChains(bot).send_keys(Keys.END).perform()
        time.sleep(2)

    row1 = bot.find_element_by_xpath(
        '//*[@id="react-root"]/section/main/article/div[2]/div/div[1]')
    row2 = bot.find_element_by_xpath(
        '//*[@id="react-root"]/section/main/article/div[2]/div/div[2]')

    r_link1 = row1.find_elements_by_tag_name('a')
    r_link2 = row2.find_elements_by_tag_name('a')
    links = r_link1 + r_link2

    urls = []

    for i in links:
        if i.get_attribute('href') != None:
            urls.append(i.get_attribute('href'))

    # ========================================================

    # Comment =====================================

    for url in urls:
        print('Commenting to this post---> ' + url)
        comment = random_comment()
        bot.get(url)
        bot.implicitly_wait(1)
        bot.execute_script("window.scrollTo(0, window.scrollY + 300)")

        time.sleep(random.randint(5, 10))

        # Like feature
        # bot.find_element_by_xpath(
        #     '/html/body/div[1]/section/main/div/div/article/div[3]/section[1]/span[1]/button').click()
        # time.sleep(2)

        bot.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/div/div/article/div[3]/section[1]/span[2]/button').click()

        if doesnt_exist(bot, '//*[@id="react-root"]/section/main/section/div'):
            print('Skiped - comments disabled')
        else:
            find_textarea = (
                By.XPATH, '//*[@id="react-root"]/section/main/section/div/form/textarea')
            WebDriverWait(bot, 50).until(
                EC.presence_of_element_located(find_textarea)
            )
            comment_box = bot.find_element(*find_textarea)
            WebDriverWait(bot, 50).until(
                EC.element_to_be_clickable(find_textarea)
            )
            comment_box.click()
            comment_box.send_keys(comment)

            time.sleep(2)

            find_button = (
                By.XPATH, '//*[@id="react-root"]/section/main/section/div/form/button')
            WebDriverWait(bot, 50).until(
                EC.presence_of_element_located(find_button)
            )
            button = bot.find_element(*find_button)
            WebDriverWait(bot, 50).until(
                EC.element_to_be_clickable(find_button)
            )
            button.click()

            time.sleep(random.randint(7, 30))

    bot.close()


while True:
    for data in datas:
        main(data)
