from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
from bs4 import BeautifulSoup
import requests
##from lxml import etree

images = []

urls_df = pd.read_csv('./urls_fixed.csv')
driver = webdriver.Chrome()
for i,url in enumerate(urls_df.values):
    driver.get(url[0])
    ##print(driver.title)
    current_url = url[0]
    try:
        confirm = driver.find_element('xpath','//*[@id="wrapper"]/div[7]/table/tbody/tr/td[1]/span/a')
        confirm.click()
        current_url = driver.current_url
    except:
        pass
    
    py_headers = ({'User-Agent':
    'Safari/537.36',\
    'Accept-Language': 'en-US, en;q=0.5'})
    webpage = requests.get(current_url, headers = py_headers)
    soup = BeautifulSoup(webpage.content, "html.parser")
    ##print(soup.find("title").text)

    tables = soup.find_all(name='table')
    try:
        rows = tables[8].find_all(name='tr')[::2]
        for row in rows:
            img = row.find(name='img')
            if img == None: continue
            img_url = img.get('src')
            final_img_url = 'https://www.getchu.com'+img_url[1:]
            images.append(final_img_url)
    except:
        pass
    if i>=1: break

print(images)




