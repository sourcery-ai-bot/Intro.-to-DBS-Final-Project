import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait              #explicit wait
from selenium.webdriver.support import expected_conditions as EC #explicit wait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

op = webdriver.ChromeOptions()
op.add_argument('--ignore-certificate-errors-spki-list')
op.add_argument('--ignore-certificate-errors')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

table=["bitcoin","usd-coin","ethereum","tether","bnb","binance-usd","xrp","dogecoin","cardano","polygon",
"multi-collateral-dai","polkadot-new","tron","litecoin","shiba-inu","solana","uniswap","avalanche","unus-sed-leo","wrapped-bitcoin"]
mapping=["Bitcoin","USD Coin","Ethereum","Tether","BNB","Binance USD","XRP","Dogecoin","Cardano","Polygon",
"Dai","Polkadot","TRON","Litecoin","Shiba Inu","Solana","Uniswap","Avalanche","UNUS SED LEO","Wrapped Bitcoin"]
db=[]
def switch_frame(target_crypto):
    driver.get(f"https://www.investing.com/crypto/{target_crypto}/historical-data")
    time.sleep(2)

driver.get("https://www.investing.com")
# time.sleep(30)
element = WebDriverWait(driver, 1000).until(
        EC.element_to_be_clickable((By.CLASS_NAME,"popupCloseIcon")) 
    )
element.click()
driver.switch_to.default_content()
time.sleep(1)

for i in range(20):
    switch_frame(table[i])
    tempt = [mapping[i]]
    datas=driver.find_elements(By.XPATH,'//*[@id="curr_table"]/tbody/tr[1]')
    tempt.extend(data.text for data in datas)
    db.append(tempt)

for i in db:
    for j in i:
        print(j," ")

driver.quit()
