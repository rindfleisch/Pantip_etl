#!/usr/bin/env python
# coding: utf-8

# In[7]:


from selenium import webdriver
from selenium.webdriver.common.by import By
import numpy as np
import pandas as pd
from time import sleep
from datetime import datetime
import locale
import pandas as pd
import sqlalchemy as sa
from urllib.parse import quote


# In[ ]:


options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options = options)

driver.get("https://pantip.com/forum/lumpini")


target_element = driver.find_elements(By.CLASS_NAME, 'col-12')
target_element


found_element = None
for i in target_element:
    #print(i.text)
    #print('___')
    if "Pantip Trend" in i.text:
       # print("found")
        found_element = i
        title_e = found_element.find_elements(By.CLASS_NAME, 'pt-list-item__title')
        name_e = found_element.find_elements(By.TAG_NAME, 'h5')
        date_e = found_element.find_elements(By.XPATH, ".//span[@title]")

        url_elements = found_element.find_elements(By.XPATH, ".//a[contains(@href, 'https://pantip.com/topic')]")

        dt_lst = []
        
                # Set locale to Thai for date parsing
        try:
            locale.setlocale(locale.LC_ALL, 'th_TH.UTF-8')
        except locale.Error:
            print("Warning: Could not set locale to 'th_TH.UTF-8'. Date parsing might fail for Thai month names.")
            # Fallback for some systems
            try:
                 locale.setlocale(locale.LC_ALL, 'Thai_Thailand.65001')
            except locale.Error:
                 print("Warning: Could not set locale to 'Thai_Thailand.65001'. Date parsing might fail.")


        for dt in date_e:
            try:
                dt = dt.get_attribute('title')
            # Remove " เวลา " and " น" for easier parsing
                dt_string_cleaned = dt.replace(" เวลา ", " ").replace(" น.", "")

                # Parse the date string
                # %d: day, %B: full month name, %Y: year, %H: hour (24-hour), %M: minute
                # Note: %Y here expects a Gregorian year. We'll adjust for Buddhist year.
                parsed_dt = datetime.strptime(dt_string_cleaned, '%d %B %Y %H:%M')

                # Adjust for Buddhist calendar year (2568 is ~2025 Gregorian)
                # The difference is typically 543 years.
                # We parse it as Gregorian and then subtract 543 from the parsed year.
                # This assumes the parsed year (e.g., 2568) was intended as Buddhist.
                gregorian_year = parsed_dt.year - 543
                # Create a new datetime object with the corrected Gregorian year
                dt_object = parsed_dt.replace(year=gregorian_year)

                dt_lst.append(dt_object)
            except ValueError as e:
                print(f"Error parsing date string '{dt}': {e}")
                dt_lst.append(None) # Append None if parsing fails
            # --- End Date Parsing ---
            #dt_lst.append(dt.get_attribute('title'))
        #full_datetime = date_e.get_attribute("title")
        title_lst = []
        name_lst = []
        #date_lst = []
        for title, name in zip(title_e, name_e):
            (title_lst.append(title.text))
            (name_lst.append(name.text))
            #(date_lst.append(date.text))
            
        urls =[]
        for url_element in url_elements:
            
            urls.append(url_element.get_attribute("href"))

        urls = list(set(urls))


df = pd.DataFrame({
"title": title_lst, "name": name_lst,
"date": dt_lst, "url": urls
})

DIALECT = "mysql"
SQL_DRIVER = "pymysql"
USERNAME = "user_de"
PASSWORD = "P@ssw0rd"
HOST = "202.44.12.115"
PORT = 3306
DBNAME = "DE_Int1"

conn_str = DIALECT + '+' + SQL_DRIVER + '://' + USERNAME + ':' + quote(PASSWORD) +'@' + HOST + ':' + str(PORT) + '/' + DBNAME

engine = sa.create_engine(conn_str,     pool_size=10,  # Adjust pool size
    pool_recycle=3600,  # Recycle connections after 1 hour
    pool_timeout=30, #adjust timeout
)
conn = engine.connect()

df.to_sql("pantip_etl_data_DE21", conn, index=False, if_exists="replace")

conn.close()


# In[ ]:





# In[ ]:




