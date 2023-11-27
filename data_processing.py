# run data_collection.py
import subprocess
# Specify the path to the Python file you want to execute
file_to_execute = 'data_collection.py'
# Use subprocess to execute the file
subprocess.run(['python', file_to_execute])

import pandas as pd
from datetime import datetime

# Extract the collected data from the "top_gainers.csv" file 
df = pd.read_csv("top_gainers_collected.csv")

# Display the first few rows of the DataFrame to verify the data
#print(df.head())

df.dtypes
number_rows = len(df)
number_nan_PE = df['PE Ratio (TTM)'].isna().sum()
#print(number_nan_PE, number_rows)
number_nan_PE / number_rows

# Change Percentage to a number between -1 and 1
def percentage_to_float(percentage_str):
    return float(percentage_str.replace('%', '')) / 100

if type(df['Percent Change'][0]) == str:
    df['Percent Change'] = df['Percent Change'].apply(percentage_to_float)
df.head()

def change_metric_and_remove_comma(number_str):
    number_str = number_str.upper()
    if ',' in number_str:
        return int(number_str.replace(',',''))
    elif 'K' in number_str:
        return int(float(number_str.replace('K',''))*(10**3))
    elif 'M' in number_str:
        return int(float(number_str.replace('M',''))*(10**6))
    elif 'B' in number_str:
        return int(float(number_str.replace('B',''))*(10**9))
    elif 'T' in number_str:
        return int(float(number_str.replace('T',''))*(10**12))
    return int(number_str)

# Drop all Nan rows that are in the 'Volume', 'Avg Vol 3 Months' and 'Market Cap' columns
#df = df.dropna(subset=['Market Cap'])
df_nan_market = df[df['Market Cap'] == 'NAN']
df_nan_volume = df[df['Volume'] == 'NAN']
df_nan_vol3mon = df[df['Avg Vol 3 Months'] == 'NAN']
df = df.drop(df_nan_market.index)
df = df.drop(df_nan_vol3mon.index)
df = df.drop(df_nan_volume.index)

# Volume write the complete number, without abbreviations units 
# and quit commas (create a function)
if type(df['Volume'][0]) == str:
    df['Volume'] = df['Volume'].apply(change_metric_and_remove_comma)
df.head()

# Avg Vol 3 Months (same as Volume)
if type(df['Avg Vol 3 Months'][0]) == str:
    df['Avg Vol 3 Months'] = df['Avg Vol 3 Months'].apply(change_metric_and_remove_comma)
df.head()


# Market Cap (same as Volume)
if type(df['Market Cap'][0]) == str:
    df['Market Cap'] = df['Market Cap'].apply(change_metric_and_remove_comma)
df.head() 


# Add the date and time of the run
# Get the current date and time
current_datetime = datetime.now()

# Add a new column with the current date and time
df['CurrentDateTime'] = current_datetime

df['CurrentDateTime'] = df['CurrentDateTime'].dt.strftime("%Y/%m/%d")


# Print the DataFrame
df.head()

df_date = df.copy()

df_date.to_csv("top_gainers_processed.csv", index=False)