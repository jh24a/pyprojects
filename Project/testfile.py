
'''
import dash_html_components as html
import io
import pandas as pd
import numpy as np
from random import random
from bs4 import BeautifulSoup
import requests

def get_corona_data():
    url="https://www.worldometers.info/coronavirus/"
    # Make a GET request to fetch the raw HTML content
    html_content = requests.get(url).text
    # Parse the html content
    soup = BeautifulSoup(html_content, "html.parser")
    gdp_table = soup.find("table", id = "main_table_countries_today")
    gdp_table_data = gdp_table.tbody.find_all("tr")

    # Getting all countries names
    dicts = {}
    for i in range(len(gdp_table_data)):
        try:
            key = (gdp_table_data[i].find_all('a', href=True)[0].string)
        except:
            key = (gdp_table_data[i].find_all('td')[0].string)

        value = [j.string for j in gdp_table_data[i].find_all('td')]
        dicts[key] = value
    live_data= pd.DataFrame(dicts).drop(0).T.iloc[:,:8]
    live_data.columns = ["Total Cases","New Cases", "Total Deaths", "New Deaths", "Total Recovered","Active","Serious Critical", "Tot Cases/1M pop"]
    live_data.index.name = 'Country'
    
    print(gdp_table_data)

    ### your file is saved here
    live_data.iloc[:,:5].to_csv("base_data.csv")

get_corona_data()
'''

import dash_html_components as html
import io
import pandas as pd
import numpy as np
from random import random
from bs4 import BeautifulSoup
import requests

def get_corona_data():
    url="https://www.worldometers.info/coronavirus/"
    # Make a GET request to fetch the raw HTML content
    html_content = requests.get(url).text
    # Parse the html content
    soup = BeautifulSoup(html_content, "html.parser")
    gdp_table = soup.find("table", id = "main_table_countries_today")
    gdp_table_data = gdp_table.tbody.find_all("tr")

    # Getting all countries names
    
    dicts = {}
    for i in range(len(gdp_table_data)):
        try:
            key = (gdp_table_data[i].find_all('a', href=True)[0].string)
        except:
            key = (gdp_table_data[i].find_all('td')[0].string)

        value = [j.string for j in gdp_table_data[i].find_all('td')]
        dicts[key] = value
    live_data= pd.DataFrame(dicts).drop(0).T.iloc[:,:8]
    live_data.columns = ["Country" , "Total Cases","New Cases", "Total Deaths", "New Deaths", "Total Recovered","Active","Critical"]
    live_data.index.name = 'Country'
    
    for key in dicts:
        print(key,'=>',dicts[key])
    print(live_data)
    ### your file is saved here
    live_data.iloc[:,:5].to_csv("base_data.csv")

get_corona_data()



