import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import requests
import shutil
from tqdm import tqdm

# Path: scraper.py

driver = webdriver.Chrome()

driver.get("https://www.shanghairanking.com/rankings/arwu/2022")
cols = ["Rank", "University", "Country", "National Rank",
        "Total Score", "Alumni", "Award", "HiCi", "N&S", "PUB", "PCP"]
import csv
file = open('data.csv', 'w+', newline ='')

data = []
for i in tqdm(range(35)):
    # get table data
    data_batch = []
    table_tag = driver.find_element(By.XPATH, '//*[@id="content-box"]/div[2]/table')
    table_body = table_tag.find_element(By.XPATH, '//*[@id="content-box"]/div[2]/table/tbody')
    table_rows = table_body.find_elements(By.TAG_NAME, "tr")
    for row in table_rows:
        table_data = row.find_elements(By.TAG_NAME, "td")
        data_point = []
        data_point.append(table_data[0].text)
        data_point.append(table_data[1].text)
        # copy inner div style
        c_name = table_data[2].find_element(By.TAG_NAME, "div").get_attribute("style")
        # find text between last / and .png
        c_name = c_name[c_name.rfind("/") + 1:c_name.rfind(".png")]
        data_point.append(c_name)

        data_point.append(table_data[3].text)
        data_point.append(table_data[4].text)

        data_batch.append(data_point)
    
        # select all options in dropdown ul tag
    # wait for dropdown to load
    
    # dropdown = driver.find_element(By.XPATH, '//*[@id="content-box"]/div[2]/table/thead/tr/th[6]/div/div[1]/div[1]')
    dropdown = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="content-box"]/div[2]/table/thead/tr/th[6]/div/div[1]/div[1]'))
    )
    
    dropdown_options = dropdown.find_elements(By.XPATH, '//*[@id="content-box"]/div[2]/table/thead/tr/th[6]/div/div[1]/div[2]')
    dropdown_options = dropdown_options[0].find_elements(By.TAG_NAME, "ul")
    dropdown_options = dropdown_options[0].find_elements(By.TAG_NAME, "li")
    
    for option in dropdown_options:
        # move mouse to option
        dropdown.click()
        ActionChains(driver).move_to_element(option).perform()
        ActionChains(driver).click().perform()

        for data_point in data_batch:
            data_point.append(table_data[5].text)
    
    # print(data_batch)

    data.extend(data_batch)
    with open('data.csv', 'a+', newline ='') as file:
        writer = csv.writer(file)
        writer.writerows(data_batch)
    # print(data)
    
    if i < 3:
        xp = '//*[@id="content-box"]/ul/li[9]/a'
    elif i==3:
        xp = '//*[@id="content-box"]/ul/li[10]/a'
    else:
        xp = '//*[@id="content-box"]/ul/li[11]/a'
    pagination_next = driver.find_element(By.XPATH, xp)
    # '//*[@id="content-box"]/ul/li[10]/a'
    # '//*[@id="content-box"]/ul/li[11]/a
    ActionChains(driver).move_to_element(pagination_next).perform()
    ActionChains(driver).click().perform()
    # time.sleep(2)
    # driver scroll to top
    driver.execute_script("window.scrollTo(0, 0);")

time.sleep(5)

# save data to csv

