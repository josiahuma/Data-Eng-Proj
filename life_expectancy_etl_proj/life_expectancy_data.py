from bs4 import BeautifulSoup
import requests
import pandas as pd
import csv
from urllib.request import urlopen


html = urlopen("https://www.worldometers.info/demographics/life-expectancy/")
soup = BeautifulSoup(html, 'html.parser')
table = soup.findAll("table", {"class":"table"})[0]
rows = table.findAll("tr")
#print(soup.prettify())

with open('/home/umajosiah/airflow-env/proj/life_expectancy_etl_proj/test.csv', 'w') as f:
     writer = csv.writer(f)
     for row in rows:
        csv_row = []
        for cell in row.findAll(["td", "th"]):
            csv_row.append(cell.get_text())
        writer.writerow(csv_row)


data = pd.read_csv(r'/home/umajosiah/airflow-env/proj/life_expectancy_etl_proj/test.csv')
pd.set_option('display.max_colwidth', None)

 #This is to rename the column names and keep the naming consistent with snake case
data.rename(columns = {'Life Expectancy  (both sexes) ':'life_expectancy(m/f)', 'Females  Life Expectancy ':'life_expectancy(f)', 'Males  Life Expectancy':'life_expectancy(m)'},  inplace=True)
print(data.head())

from sqlalchemy import create_engine
import os
import psycopg2

# Database Credentials
username = os.environ['USER']
password = os.environ['PASSWORD']
host = 'winhost'
port = 5433
db_name = 'Life_Expectancy_Airflow'

# Establish a connection
engine = create_engine(f'postgresql://{username}:{password}@{host}:{port}/{db_name}')
#Load the database table - employee_table

data.to_sql('life_expectancy_data', engine, if_exists='replace', index=False)

# Close the connection
engine.dispose()