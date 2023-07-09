from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd
from bs4 import BeautifulSoup
import requests
import time


## Headers
py_headers = ({'User-Agent':
'Safari/537.36',\
'Accept-Language': 'en-US, en;q=0.5'})

## Variable Declaration
delay = 20
total_time =0

def load_data(filepath):
    ## Loading URLS from csv
    urls_df = pd.read_csv(filepath)
    urls = [url[0] for url in urls_df.values]
    return urls

def get_current_url(url,driver):
    ## Bypassing age checking on to actual webpage
    ## Checking if page will load, else refresh the page
    driver=driver; driver.get(url)
    try: myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located(('xpath','//*[@id="wrapper"]/div[7]/table/tbody/tr/td[1]/span/a')))
    except TimeoutException: print("Loading took too much time!"); driver.refresh()
    try:
        confirm = driver.find_element('xpath','//*[@id="wrapper"]/div[7]/table/tbody/tr/td[1]/span/a')
        confirm.click()
        current_url = driver.current_url
    except: pass  
    return current_url

def write_to_file(filename,container_num):
    ## Writing image to file
    with open(f'./images/{filename}', 'wb') as file:
        file.write(driver.find_element('xpath',f'//*[@id="wrapper"]/table[4]/tbody/tr[{container_num}]/td[1]/img').screenshot_as_png)
        file.close()
    pass

def Scrape(url,driver):
    ## Check if image containers are in webpage tables
    ## If present, download images
    ## Returns runtime per url
    start_time = time.time()
    current_url = get_current_url(url,driver)
    webpage = requests.get(current_url, headers = py_headers)
    soup = BeautifulSoup(webpage.content, "html.parser")

    tables = soup.find_all(name='table')
    l=0
    for table in tables:
        try:
            if "キャ" in table.find_all("img")[0].get("alt"):
                rows = table.find_all(name='tr')[::2]
                k=1
                for j,row in enumerate(rows):
                    img = row.find(name='img')
                    if img == None: continue                     
                    img_url = img.get('src')
                    filename = img_url[1:].split("/")[-1].replace("jpg","png")
                    write_to_file(filename,k)
                    k+=2; l+=1
        except Exception as e: continue

    print("From",url,"Successfully retrieved",l,"images", end="    ")
    end_time = time.time() - start_time
    print("--- %s seconds ---" % (end_time))
    return end_time

## MAIN
if __name__ == '__main__':
    urls = load_data('./urls_fixed.csv')
    for i,url in enumerate(urls):
        driver = webdriver.Chrome()
        total_time += Scrape(url,driver)
        driver.close()
        if i>=10: break ## Tester Only. Comment for full run.
    print("\nTotal runtime --- %.2f minutes ---" % (total_time/60))





########
########

##    images = []
##    total_time = 0.0
##    delay = 20 # seconds
##    urls_df = pd.read_csv('./urls_fixed.csv')
##    for i,url in enumerate(urls_df.values):
##        start_time = time.time()
##        print("Getting from:",url[0], end=" ")
##        driver = webdriver.Chrome()
##        driver.get(url)
##        try:
##            myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located(('xpath','//*[@id="wrapper"]/div[7]/table/tbody/tr/td[1]/span/a')))
##    ##        print("Page is ready!")
##        except TimeoutException:
##            print("Loading took too much time!")
##        current_url = url
##        try:
##            confirm = driver.find_element('xpath','//*[@id="wrapper"]/div[7]/table/tbody/tr/td[1]/span/a')
##            confirm.click()
##            current_url = driver.current_url
##        except:
##            pass
##
##        webpage = requests.get(current_url, headers = py_headers)
##        soup = BeautifulSoup(webpage.content, "html.parser")
##
##        tables = soup.find_all(name='table')
##        for table in tables:
##            try:
##                if "キャ" in table.find_all("img")[0].get("alt"):
##                    rows = table.find_all(name='tr')[::2]
##                    k=1
##                    l=0
##                    for j,row in enumerate(rows):
##                        img = row.find(name='img')
##                        if img == None: continue                     
##                        img_url = img.get('src')
##    ##                    final_img_url = 'https://www.getchu.com'+img_url[1:]
##                        filename = img_url[1:].split("/")[-1].replace("jpg","png")
##                        with open(f'./images/{filename}', 'wb') as file:
##                            file.write(driver.find_element('xpath',f'//*[@id="wrapper"]/table[4]/tbody/tr[{k}]/td[1]/img').screenshot_as_png)
##                        file.close()
##                        k+=2; l+=1
##    ##                    filename=path+"/"+str(i)+'_'+str(j)+'.jpeg'
##    ##                    urlretrieve(final_img_url,filename)
##    ##                    images.append(final_img_url)
##            except Exception as e:
##                continue
##            
##        print("Successfully retrieved",l,"images", end="    ")
##        driver.close()
##        end_time = time.time() - start_time
##        print("--- %s seconds ---" % (end_time))
##        total_time += end_time
##        if i>=1: m=i; break
##
##        
##    print("\nTotal Execution Time --- %s minutes ---" % (total_time/60))
##    print("Average Time per URL --- %s seconds ---" % (total_time/m))
##
##
