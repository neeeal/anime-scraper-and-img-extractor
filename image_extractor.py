from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
from bs4 import BeautifulSoup
import requests
##from urllib.request import urlretrieve

images = []

urls_df = pd.read_csv('./urls_fixed.csv')
for i,url in enumerate(urls_df.values):
    driver = webdriver.Chrome()
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
    for table in tables:
        try:
            if "キャ" in table.find_all("img")[0].get("alt"):
                rows = table.find_all(name='tr')[::2]
                for j,row in enumerate(rows):
                    img = row.find(name='img')
                    if img == None: continue
                    img_url = img.get('src')
                    final_img_url = 'https://www.getchu.com'+img_url[1:]
##                    filename=path+"/"+str(i)+'_'+str(j)+'.jpeg'
##                    urlretrieve(final_img_url,filename)
                    images.append(final_img_url)
        except Exception as e: print(e)

    driver.close()
    print(images)
    if i>=3: break

print(images)
with open('image_urls.txt','w') as tfile:
	tfile.write('\n'.join(images))
	




