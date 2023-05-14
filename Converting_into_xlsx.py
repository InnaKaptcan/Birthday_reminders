# Преобразуем таблицу в формат xlsx (иначе библиотека openpyxl не сможет ее прочитать)

import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from Days_of_interest import todays_file_name

os.chdir("/Users/innakaptcan/Downloads")

chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(options=chrome_options)
# driver = webdriver.Chrome()
driver.implicitly_wait(50)
driver.get('https://convertio.co/xls-xlsx/')

choose_file = driver.find_element(By.NAME, "pc-upload")
file_location = os.path.join(os.getcwd(), todays_file_name + '.xls')
choose_file.send_keys(file_location)

driver.find_element(By.CLASS_NAME, "convert-button").click()
driver.find_element(By.LINK_TEXT, "Download").click()
driver.find_element(By.LINK_TEXT, "Download").click()

driver.quit()
