import requests
from bs4 import BeautifulSoup
from time import sleep
from random import randint
import numpy as np
import pandas as pd
import re

def run_laptop_etl():

    #declaring the list of empty variables, so that we can append the data overall

    acc_name = []
    lap_state = []
    lap_price = []

    #creating an array of values and passing it in the url for dynamic webpages
    pages = np.arange(1,50,1)

    #the whole core of the script
    for page in pages:
        page = requests.get("https://www.ebay.co.uk/e/_electronics/techsale-up-to-60-off-dell-laptops?_dmd=1&rt=nc&_pgn="+str(page))
        soup = BeautifulSoup(page.text, 'html.parser')
        #print(soup.prettify())
        acc_data = soup.find_all('div', {'class': 's-item__info clearfix'})
        sleep(randint(2,6))
        #print(acc_data[0])
        for store in acc_data:
            name = store.find('h3', {'class': 's-item__title'}).text
            acc_name.append(name)
            
            state = store.find('span', {'class': 's-item__certified-refurbished s-item__certified-refurbished--isLarge'}).text
            lap_state.append(state)
            
            price = store.find('span', {'class': 's-item__price'}).text
            lap_price.append(price)
            
    data = pd.DataFrame({"Lap detail": acc_name, "Laptop State": lap_state, "Laptop Price": lap_price})

    #print(data.head())

    data.to_csv('/home/umajosiah/airflow-env/proj/laptop_etl_proj/ebay_laptops.csv', index=None)

    data = pd.read_csv(r'/home/umajosiah/airflow-env/proj/laptop_etl_proj/ebay_laptops.csv')
    pd.set_option('display.max_colwidth', None)
    data.head()

    data['Drive Size'] = data['Lap detail'].str.extract(r'(64|120|240|128|160|255|256|500)GB')

    data['RAM'] = data['Lap detail'].str.extract(r'(RAM|Ram|ram)')

    data['RAM Size'] = data['Lap detail'].str.extract(r'(2GB|2gb|3GB|3gb|4GB|4gb|6GB|6gb|8GB|8gb|12GB|12gb|16GB|16gb|32GB|32gb|64GB|64gb)')

    #This is to help create "Lap OS" column
    data['Laptop OS'] = np.where(data['Lap detail'].str.contains(r'(?:WINDOWS 11|Windows 11|win11)'), "Windows",
                        np.where(data['Lap detail'].str.contains(r'(?:macOS|mac OS|Mac|MAC|Macbook Pro|mac)'), "Mac OS",
                        np.where(data['Lap detail'].str.contains(r'(?:chrome|CHROMEBOOK)'), "Chromebook","Unspecified OS")))

    #This is to help create "Drive Type" column
    data['Drive Type'] = np.where(data['Lap detail'].str.contains(r'(?:SSD|ssd)'), "SSD",
                        np.where(data['Lap detail'].str.contains(r'(?:HDD|hdd|Hard Disk|Hdd|Harddisk)'), "HDD", "Unspecified Disk Type"))

    # #This is to help create "Processor Type" column
    data['Processor Type'] = np.where(data['Lap detail'].str.contains(r'(?:dual core|Dual Core|DUAL CORE)'),"Intel Dual Core",
                            np.where(data['Lap detail'].str.contains(r'(?:core i3|Core i3|CORE i3)'),"Intel Core i3",
                            np.where(data['Lap detail'].str.contains(r'(?:core i5|Core i5|CORE i5)'),"Intel Core i5",
                            np.where(data['Lap detail'].str.contains(r'(?:core i7|Core i7|CORE i7)'),"Intel Core i7",
                            np.where(data['Lap detail'].str.contains(r'(?:core i9|Core i9|CORE i9)'),"Intel Core i9",
                            np.where(data['Lap detail'].str.contains(r'(?:ryzen 3|Ryzen 3|RYZEN 3)'),"AMD Ryzen 3",
                            np.where(data['Lap detail'].str.contains(r'(?:ryzen 5|Ryzen 5|RYZEN 5)'),"AMD Ryzen 5",
                            np.where(data['Lap detail'].str.contains(r'(?:ryzen 7|Ryzen 7|RYZEN 7)'),"AMD Ryzen 7",
                            np.where(data['Lap detail'].str.contains(r'(?:ryzen 9|Ryzen 9|RYZEN 9)'),"AMD Ryzen 9","Others")))))))))

    #This is to help create "Laptop Brand" column
    data['Laptop Brand'] = np.where(data['Lap detail'].str.contains(r'(?:Apple|apple|Mac|APPLE|mac|MAC)'),"Apple",
                        np.where(data['Lap detail'].str.contains(r'(?:Hp|hp|HP)'),"HP",
                        np.where(data['Lap detail'].str.contains(r'(?:Lenovo|lenovo|LENOVO)'),"Lenovo",
                        np.where(data['Lap detail'].str.contains(r'(?:Dell|dell|DELL)'),"Dell",
                        np.where(data['Lap detail'].str.contains(r'(?:Acer|acer|ACER)'),"Acer",
                        np.where(data['Lap detail'].str.contains(r'(?:Asus|asus|ASUS)'),"Asus",
                        np.where(data['Lap detail'].str.contains(r'(?:MSI|msi|Msi)'),"MSI",
                        np.where(data['Lap detail'].str.contains(r'(?:Microsoft Surface|Surface|Microsoft|microsoft)'),"Microsoft Surface",
                        np.where(data['Lap detail'].str.contains(r'(?:ryzen|Ryzen|RYZEN)'),"Razer",
                        np.where(data['Lap detail'].str.contains(r'(?:samsung|Samsung|SAMSUNG)'),"Samsung","Other Brand"))))))))))

    #This is to rename the column names and keep the naming consistent with snake case
    data.rename(columns = {'Lap detail':'lap_detail', 'Laptop State':'laptop_state', 'Laptop Price':'laptop_price', 'Drive Size':'drive_size',
                        'RAM':'ram', 'RAM Size':'ram_size', 'Laptop OS':'laptop_os', 'Lap OS':'lap_os', 'Drive Type':'drive_type',
                        'Processor Type':'processor_type', 'Laptop Brand':'laptop_brand'}, inplace = True)

    #Replace every instance of comma with empty string
    data['lap_detail']=data['lap_detail'].str.replace(',','')
    data['laptop_price']=data['laptop_price'].str.replace(',','')

    data.to_csv('/home/umajosiah/airflow-env/proj/laptop_etl_proj/laptops.csv', index = None)


    from sqlalchemy import create_engine
    import os
    import psycopg2

    # Database Credentials
    username = os.environ['USER']
    password = os.environ['PASSWORD']
    host = 'winhost'
    port = 5433
    db_name = 'Ebay_Laptops_Airflow'
    
    conn = None 
    cur = None 
    try: 
        conn = psycopg2.connect(host = host, dbname = db_name, user = username, password = password, port = port)
        cur = conn.cursor()
        cur.execute('DROP TABLE IF EXISTS laptops')
        create_script = '''CREATE TABLE IF NOT EXISTS laptops (
                        Lap_detail varchar(300) NOT NULL,
                        laptop_state varchar(50),
                        laptop_price varchar(50),
                        drive_size varchar(50),
                        ram varchar(50),
                        ram_size varchar(10),
                        laptop_os varchar(50),
                        drive_type varchar(50),
                        processor_type varchar(50),
                        laptop_brands varchar(50))'''
        cur.execute(create_script) 
        with open('/home/umajosiah/airflow-env/proj/laptop_etl_proj/laptops.csv', 'r', encoding="ISO-8859-1") as f: 
            next(f) #This skips the header row.
            cur.copy_from(f, 'laptops', sep=',')
            conn.commit()
    except Exception as error: 
        print(error)
    finally: 
        if cur is not None: 
            cur.close() 
        if conn is not None: 
            conn.close()