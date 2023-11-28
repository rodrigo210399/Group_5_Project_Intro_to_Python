import os
import pandas as pd
import sqlite3

# Path to the folder containing CSV files (company_datasets)
csvs_folder = 'company_datasets'

# Path to the folder where SQLite files will be saved (company_databases)
sqlite_folder = 'company_databases'

# Get the current working directory (where the this file is located)
current_directory = os.getcwd()

# Full paths to the CSV and SQLite folders
full_csvs_folder = os.path.join(current_directory, csvs_folder)
full_sqlite_folder = os.path.join(current_directory, sqlite_folder)

# Create the SQLite folder if it doesn't exist
os.makedirs(full_sqlite_folder, exist_ok=True)

# Loop through each CSV file in the CSVs folder
for csv_file in os.listdir(full_csvs_folder):
    if csv_file.endswith('_data.csv'):
        # Extract the name from the CSV file (assuming the name is before '_data.csv')
        name = os.path.splitext(csv_file)[0].replace('_data', '')

        # Read CSV file into a DataFrame
        df = pd.read_csv(os.path.join(full_csvs_folder, csv_file))

        # Create SQLite database connection
        db_file = os.path.join(full_sqlite_folder, f'{name}_database.db')
        db_connection = sqlite3.connect(db_file)

        # Write the DataFrame to a table in the database
        df.to_sql(name, db_connection, index=False, if_exists='replace')

        # Close the database connection
        db_connection.close()

        #print(f"CSV file '{csv_file}' converted to SQLite file '{db_file}'.")
