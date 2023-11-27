import pandas as pd
import os

# run data_processing.py after running datacollection.py
import subprocess
# Specify the path to the Python file you want to execute
file_to_execute = 'data_processing.py'
# Use subprocess to execute the file
subprocess.run(['python', file_to_execute])

# Read the csv file associated with the market top gainers
df = pd.read_csv("top_gainers_processed.csv")
# Create a directory to store the databases if it does not exist
database_dir = 'company_datasets'
if not os.path.exists(database_dir):
    os.makedirs(database_dir)

# List of column headers
column_headers = ['Name','Last Price', 'Change', 'Percent Change', 'Volume',
                  'Avg Vol 3 Months', 'Market Cap', 'PE Ratio (TTM)', 'CurrentDateTime']

# Create an empty dictionary to store dataframes
id_dataframes = {}

# Iterate over unique IDs
for unique_id in df['Symbol'].unique():
    # Create a dataframe for each unique ID
    id_dataframe = df[df['Symbol'] == unique_id].copy()
    
    # Add the dataframe to the dictionary with the ID as the key
    id_dataframes[unique_id] = id_dataframe.drop_duplicates()

output_directory = "company_datasets"

# Create the output directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Iterate through the dictionary and save each dataframe to a CSV file
for key, df in id_dataframes.items():
    # Construct the CSV file path based on the ID
    csv_file_path = os.path.join(output_directory, f"{key}_data.csv")
    # Check if the CSV file already exists
    if os.path.exists(csv_file_path):
        # If the CSV file exists, read the existing data and concatenate with the new data
        existing_data = pd.read_csv(csv_file_path)
        combined_data = pd.concat([existing_data, df], ignore_index=True)
        combined_data.to_csv(csv_file_path, index=False, header=True)  # mode='w' to overwrite the file
    else:
        # If the CSV file doesn't exist, save the dataframe directly
        df.to_csv(csv_file_path, index=False)

# Assuming the CSV files are in the output_directory
# Set the maximum number of rows per CSV file
max_rows_per_file = 100

# ...

# Iterate through the CSV files in the output directory
for file_name in os.listdir(output_directory):
    if file_name.endswith(".csv"):
        # Construct the full path to the CSV file
        csv_file_path = os.path.join(output_directory, file_name)

        # Read the CSV file into a dataframe
        df = pd.read_csv(csv_file_path)

        # Remove duplicate rows
        df_cleaned = df.drop_duplicates()

        # Check if the number of rows exceeds the limit
        if len(df_cleaned) > max_rows_per_file:
            # Trim the dataframe to the last max_rows_per_file rows
            df_cleaned = df_cleaned.tail(max_rows_per_file)

        # Save the cleaned dataframe to a new CSV file
        cleaned_file_path = os.path.join(output_directory, f"{file_name}")
        df_cleaned.to_csv(cleaned_file_path, header=True, index=False, mode='w')  
        # 'w' to overwrite the file

# ...

# Display information about cleaned files
#print("Data processing and cleaning completed.")
