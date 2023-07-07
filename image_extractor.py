from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd

urls_df = pd.read_csv('./urls_fixed.csv')

driver = webdriver.Chrome('./chromedriver')

driver.get(urls_df.values[0])
print(driver.title)
