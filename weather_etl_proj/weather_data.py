import json
import requests # It is a popular HTTP library for HTTP requests in Python
import pandas as pd # It is a powerful, open-source data manipulation and analysis library for Python
from datetime import datetime # The datetime module supplies classes to work with date and time
import matplotlib.pyplot as plt # For Data visualisation
import seaborn as sns # For Data visualisation
import psycopg2 # For connecting to PstgreSQL databases and executing queries.
from sqlalchemy import create_engine # To efficiently manage and reuse database connections

def run_weather_etl():
      

    url = f"https://api.open-meteo.com/v1/forecast?latitude=52.9536&longitude=-1.1505&daily=temperature_2m_max,temperature_2m_min,apparent_temperature_max,apparent_temperature_min,daylight_duration,sunshine_duration,rain_sum,showers_sum,snowfall_sum,wind_speed_10m_max&timezone=Europe%2FLondon"

    response = requests.get(url)


    data = response.json()
    json_str = json.dumps(data, indent=4)
    print(json_str)


    def convert(seconds):
        min, sec = divmod(seconds, 60)
        hour, min = divmod(min, 60)
        return '%d:%02d:%02d' % (hour, min, sec)


    data = response.json()
    weather_data = []
    count = 0
    for day in data['daily']['time']:
        time = data['daily']['time'][count]
        temp_max = data['daily']['temperature_2m_max'][count]
        temp_min = data['daily']['temperature_2m_min'][count]
        daylight = data['daily']['daylight_duration'][count]
        daylight_hrs = convert(data['daily']['daylight_duration'][count])
        sunshine = data['daily']['sunshine_duration'][count]
        sunshine_hrs = convert(data['daily']['sunshine_duration'][count])
        rain_vol = data['daily']['rain_sum'][count]
        snowfall = data['daily']['snowfall_sum'][count]
        wind_speed = data['daily']['wind_speed_10m_max'][count]

            
        weather_data.append({
            "Date": time,
            "Max Temperature": temp_max,
            "Min Temperature": temp_min,
            "Daylight Duration (seconds)": daylight,
            "Daylight Duration (hours)": daylight_hrs,
            "Sunshine Duration (seconds)": sunshine,
            "Sunshine Duration (hours)": sunshine_hrs,
            "Rain Volumn (mm)": rain_vol,
            "Snowfall (cm)": snowfall,
            "Wind Speed": wind_speed    
            })
        count += 1
            
        df = pd.DataFrame(weather_data)
        
    df.head(10)


    df.info()



    min_average_value = df['Min Temperature'].mean()
    max_average_value = df['Max Temperature'].mean()

    plt.figure(figsize=(10,4))
    plt.plot(df['Date'], df['Min Temperature'], color='red', marker='p', linestyle='dashed', linewidth=2, markersize=12)
    plt.plot(df['Date'], df['Max Temperature'], color='green', marker='p', linestyle='dashed', linewidth=2, markersize=12)
    plt.axhline(y=max_average_value, color='g', linestyle='--', label=f'Max Average = {max_average_value:.2f}')
    plt.axhline(y=min_average_value, color='r', linestyle='--', label=f'Min Average = {min_average_value:.2f}')
    plt.title('Max Vs Min Temperature')
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.legend(loc='upper left') # Add a legend
    plt.grid(True)
    #plt.show()
    plt.savefig('/home/umajosiah/airflow-env/proj/weather_etl_proj/Temperature_graph.png')


    rain_value = df['Rain Volumn (mm)'].sum()

    plt.figure(figsize=(10,4))
    plt.plot(df['Date'], df['Rain Volumn (mm)'], color='red', marker='p', linestyle='dashed', linewidth=2, markersize=12)
    # plt.axhline(y=rain_value, color='g', linestyle='--', label=f'Max Average = {rain_value:.2f}')
    plt.title('Rain Volumn Temperature')
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.legend(loc='upper left') # Add a legend
    plt.grid(True)
    #plt.show()
    plt.savefig('/home/umajosiah/airflow-env/proj/weather_etl_proj/Rain_graph.png')


    # Database Credentials
    from sqlalchemy import create_engine
    import os
    import psycopg2

    # Database Credentials
    username = os.environ['USER']
    password = os.environ['PASSWORD']
    host = 'winhost'
    port = 5433
    db_name = 'Weather_Data_Airflow'


    # Establish a connection
    engine = create_engine(f'postgresql://{username}:{password}@{host}:{port}/{db_name}')


    #Load the database table - employee_table

    df.to_sql('weather_data', engine, if_exists='replace', index=False)

    # Close the connection
    engine.dispose()