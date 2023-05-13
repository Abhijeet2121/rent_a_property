from bs4 import BeautifulSoup
import requests
import lxml
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

URL = "https://www.zillow.com/daly-city-ca/rentals/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22north%22%3A37.72017194334965%2C%22east%22%3A-122.39112040429686%2C%22south%22%3A37.63675270856502%2C%22west%22%3A-122.5147165957031%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A31163%2C%22regionType%22%3A6%7D%5D%2C%22mapZoom%22%3A13%7D"

header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}

response = requests.get(URL, headers=header)
data = response.text
soup = BeautifulSoup(data, 'html.parser')

links = soup.select("article a")
all_links = []
for link in links:
    href = link['href']
    # print(href)
    if "http" not in href:
        all_links.append(f"https://www.zillow.com{href}")
    else:
        all_links.append(href)
    
address_ele = soup.select("article a address")
all_addresses = [address.get_text().split(" | ")[-1] for address in address_ele]
# print(all_address)

prices = soup.select("article div div div span")
all_prices = [price.get_text().split("+")[0] for price in prices if "$" in price.text]
# print(all_prices)

# for price in prices:
#     if "$" in price.text:
#         formatted_price = (price.get_text().split("+")[0])


# for address in address_ele:
#     formatted_add = address.get_text().split("|")[-1]
#     all_address.append(formatted_add)
# print(all_address)

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
options.page_load_strategy = 'none'

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)

for n in range(len(all_links)):
    time.sleep(2)

    driver.get('https://docs.google.com/forms/d/e/1FAIpQLSdgvRxC6SPM39jc3Wa6nNtj13ZjCxLHl2uzKOGbsVxD6bwPAw/viewform?usp=sf_link')
    time.sleep(2)

    address = driver.find_element(By.XPATH, "/html/body/div/div[2]/form/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input")
    address.send_keys(all_addresses[n])

    prices = driver.find_element(By.XPATH, '/html/body/div/div[2]/form/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    prices.send_keys(all_prices[n])

    links = driver.find_element(By.XPATH, '/html/body/div/div[2]/form/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    links.send_keys(all_links[n])

    submit = driver.find_element(By.XPATH, "/html/body/div/div[2]/form/div[2]/div/div[3]/div[1]/div[1]/div/span/span")
    submit and submit.click()
   
    