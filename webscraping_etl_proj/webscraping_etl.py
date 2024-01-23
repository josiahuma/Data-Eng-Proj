# Step 1: Import your libraries
import pandas as pd
import psycopg2 # For connect to postgresql databases and executing queries
from sqlalchemy import create_engine # To efficiently manage and reuse database connections
import os


url = "https://www.worldometers.info/world-population/nigeria-population/"

table1 = pd.read_html(url)[1]
table2 = pd.read_html(url)[2]
table3 = pd.read_html(url)[3]

# View the first 5 rows
#table1.head()
#table2.head()
#table3.head()

# Transform column headers
# Eliminate all the spaces in the column headers
table1.columns = ['Year', 'Population', 'Yearly%Change', 'YearlyChange',
       'Migrants(net)', 'MedianAge', 'FertilityRate', 'Density(P/Km²)',
       'UrbanPop%', 'UrbanPopulation', 'ShareofWorldPop',
       'WorldPopulation', 'NigeriaGlobalRank' 
]

table2.columns = ['Year', 'Population', 'Yearly%Change', 'YearlyChange',
       'Migrants(net)', 'MedianAge', 'FertilityRate', 'Density(P/Km²)',
       'UrbanPop%', 'UrbanPopulation', 'ShareofWorldPop',
       'WorldPopulation', 'NigeriaGlobalRank'
]

table3.columns = ['SerialNumber', 'CITYNAME', 'POPULATION']

# View the transformed headers
#table1.columns
#table2.columns
#table3.columns

# Load data in PostgreSQL Database 

# Database Credentials
username = os.environ['USER']
password = os.environ['PASSWORD']
host = 'winhost'
port = 5433
db_name = 'Naija_Population'

# Establish a connection
engine = create_engine(f'postgresql://{username}:{password}@{host}:{port}/{db_name}')

# Create variables to hold table names
dbt1 = 'pop_historical'
dbt2 = 'pop_forecast'
dbt3 = 'pop_city'

#Load data into database tables
table1.to_sql(dbt1, engine, if_exists='replace', index=False)
table2.to_sql(dbt2, engine, if_exists='replace', index=False)
table3.to_sql(dbt3, engine, if_exists='replace', index=False)

# Close connection
engine.dispose()