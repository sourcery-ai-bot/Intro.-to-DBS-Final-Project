import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait  # explicit wait
from selenium.webdriver.support import expected_conditions as EC  # explicit wait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

op = webdriver.ChromeOptions()
op.add_argument('--ignore-certificate-errors-spki-list')
op.add_argument('--ignore-certificate-errors')


def OpenDriver():
    global driver
    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), chrome_options=op)


table = ["bitcoin", "usd-coin", "ethereum", "tether", "bnb", "binance-usd", "xrp", "dogecoin", "cardano", "polygon",
         "multi-collateral-dai", "polkadot-new", "tron", "litecoin", "shiba-inu", "solana", "uniswap", "avalanche",
         "unus-sed-leo", "wrapped-bitcoin"]
mapping = ["Bitcoin", "USD Coin", "Ethereum", "Tether", "BNB", "Binance USD", "XRP", "Dogecoin", "Cardano", "Polygon",
           "Dai", "Polkadot", "TRON", "Litecoin", "Shiba Inu", "Solana", "Uniswap", "Avalanche", "UNUS SED LEO",
           "Wrapped Bitcoin"]
db = []
crawl_first_called = False


def switch_frame(target_crypto):
    global driver
    driver.get("https://www.investing.com/crypto/" +
               target_crypto + "/historical-data")
    time.sleep(1)
    try:
        driver.find_element(By.CLASS_NAME, 'takeover').click()
        driver.switch_to.window(driver.window_handles[0])
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, '/html/body/div[5]/section/div[7]/div[4]/table[1]/tbody/tr[1]/td[1]')))
        # time.sleep(5)
    except NoSuchElementException:
        time.sleep(1)
    # time.sleep(1)


def getList(i):
    global driver
    tempt = [mapping[i]]
    # datas=driver.find_elements(By.XPATH,'//*[@id="curr_table"]/tbody/tr[1]')
    date = driver.find_element(
        By.XPATH, '/html/body/div[5]/section/div[7]/div[4]/table[1]/tbody/tr[1]/td[1]')
    tempt.append(date.text)
    price = driver.find_element(
        By.XPATH, '/html/body/div[5]/section/div[7]/div[4]/table[1]/tbody/tr[1]/td[2]')
    tempt.append(price.text)
    ope = driver.find_element(
        By.XPATH, '/html/body/div[5]/section/div[7]/div[4]/table[1]/tbody/tr[1]/td[3]')
    tempt.append(ope.text)
    high = driver.find_element(
        By.XPATH, '/html/body/div[5]/section/div[7]/div[4]/table[1]/tbody/tr[1]/td[4]')
    tempt.append(high.text)
    low = driver.find_element(
        By.XPATH, '/html/body/div[5]/section/div[7]/div[4]/table[1]/tbody/tr[1]/td[5]')
    tempt.append(low.text)
    vol = driver.find_element(
        By.XPATH, '/html/body/div[5]/section/div[7]/div[4]/table[1]/tbody/tr[1]/td[6]')
    tempt.append(vol.text)
    change = driver.find_element(
        By.XPATH, '/html/body/div[5]/section/div[7]/div[4]/table[1]/tbody/tr[1]/td[7]')
    tempt.append(change.text)
    return tempt


def crawl():
    global driver
    driver.get("https://www.investing.com")
    # time.sleep(30)
    element = WebDriverWait(driver, 1000).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "popupCloseIcon"))
    )
    element.click()
    driver.switch_to.default_content()
    time.sleep(1)

    for i in range(20):
        switch_frame(table[i])
        tempt = getList(i)
        # print(datas.text)
        # for data in datas:
        #     tempt.append(data.text)
        db.append(tempt)
        print(i * 5 + 5, '%')

    # for i in db:
    #     print(i)

    driver.quit()
    return db
