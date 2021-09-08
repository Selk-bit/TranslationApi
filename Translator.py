from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options
import random
from difflib import SequenceMatcher



def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

SourceLanguageSelectXpath = '//*[@id="dl_translator"]/div[4]/div[4]/div[1]/div[1]/div/button'
DestLanguageSelectXpath = '//*[@id="dl_translator"]/div[4]/div[4]/div[3]/div[1]/div[2]/div[1]/button'
sourceLanguagesListXpath = '//*[@id="dl_translator"]/div[4]/div[4]/div[1]/div[1]/div/button'
destLanguagesListXpath = '//*[@id="dl_translator"]/div[4]/div[4]/div[3]/div[1]/div[2]/div[1]/div[2]'
languageXpath = './/button'
sourceTextAreaXpath = '//*[@id="dl_translator"]/div[4]/div[4]/div[1]/div[2]/div[2]/textarea'
destTextAreaXpath = '//*[@id="dl_translator"]/div[4]/div[4]/div[3]/div[3]/div[1]/textarea'
yassineDiv = '//*[@id="target-dummydiv"]'
destSpanXpath = '//*[@id="dl_translator"]/div[4]/div[4]/div[3]/div[3]/div[1]/div/span[3]'
copyButtonXpath = '//*[@id="dl_translator"]/div[4]/div[4]/div[3]/div[3]/div[4]/p/button'

width = random.randint(1000, 2000)
height = random.randint(500, 1000)
chrome_options = Options()

chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 640 XL LTE) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Mobile Safari/537.36 Edge/12.10166")

webdriver.DesiredCapabilities.CHROME['acceptSslCerts'] = True
chrome_options.add_experimental_option("useAutomationExtension", False)
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_argument('disable-infobars')
chrome_options.add_argument('--disable-web-security')
chrome_options.add_argument("--disable-blink-features")
chrome_options.add_argument('--profile-directory=Default')
chrome_options.add_argument('--allow-running-insecure-content')
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
#chrome_options.add_argument("--headless")
chrome_options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
chrome_options.add_argument("window-size=" + str(width) + "," + str(height))
driver = webdriver.Chrome("./chromedriver", options=chrome_options)
driver.maximize_window()
driver.get('https://www.deepl.com/translator')
sleep(random.randint(1, 2))
coockie = {'domain': '.deepl.com', 'expiry': 4784272610, 'httpOnly': True, 'name': 'dl_session', 'path': '/',
           'secure': True,
           'value': '4d4b1a36-f411-aeb0-8490-670d54e24e22'}
driver.add_cookie(coockie)
sleep(1)
driver.get('https://www.deepl.com/translator')
sleep(1)
driver.get('https://www.deepl.com/translator')


def Deepl(source, dest, content):
    driver.find_element_by_xpath(SourceLanguageSelectXpath).click()
    sleep(0.1)
    languageList = driver.find_element_by_xpath(sourceLanguagesListXpath)
    languages = languageList.find_elements_by_xpath(languageXpath)
    languages = languages[1:]
    for language in languages:
        # driver.execute_script("arguments[0].scrollIntoView();", language)
        if similar(language.text, source) > 0.8:
            language.click()
            break
    driver.find_element_by_xpath(DestLanguageSelectXpath).click()
    sleep(0.1)
    languageList = driver.find_element_by_xpath(destLanguagesListXpath)
    languages = languageList.find_elements_by_xpath(languageXpath)
    languages = languages[1:]
    if similar('Chinese', dest) > 0.8:
        dest = 'Chinese (simplified)'
    if similar('English', dest) > 0.8:
        dest = 'English (American)'
    if similar('Portuguese', dest) > 0.8:
        dest = 'Portuguese (Brazilian)'
    for language in languages:
        if similar(language.text, dest) > 0.8:
            language.click()
            break
    length = 0
    res = isinstance(content, str)
    if not res:
        for i in content:
            length += len(i)
    else:
        length = len(content)
    driver.find_element_by_xpath(sourceTextAreaXpath).clear()
    driver.find_element_by_xpath(sourceTextAreaXpath).send_keys(content)
    if dest == 'Chinese (simplified)' or similar('Japanese', dest) > 0.8:
        sleep(3)
        src = driver.page_source
        translated = src.split("<div id=\"target-dummydiv\" class=\"lmt__textarea lmt__textarea_dummydiv\">")[1].split('</div>')[0]
    else:
        while True:
            src = driver.page_source
            translated = src.split("<div id=\"target-dummydiv\" class=\"lmt__textarea lmt__textarea_dummydiv\">")[1].split('</div>')[0]
            loweredTranslated = translated.lower()
            print(len(translated))
            print(length)
            if loweredTranslated.islower() and len(translated)-2 > length/2 and '[...]' not in translated:
                break
            sleep(0.1)
    uses = 1
    return translated