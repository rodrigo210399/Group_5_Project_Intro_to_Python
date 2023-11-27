import requests
from bs4 import BeautifulSoup
import pandas as pd

# Define a function to scrape the top stock gainers from yahoo finance
def scrape_gainers_page(page_number):
    url = f"https://finance.yahoo.com/gainers?offset={page_number * 25}"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        gainer_table = soup.find('table')

        data = []
        for row in gainer_table.find_all('tr')[1:]:  # Skip the header row
            cols = row.find_all('td')
            symbol = cols[0].text
            name = cols[1].text
            last_price = cols[2].text
            change = cols[3].text
            percent_change = cols[4].text
            volume = cols[5].text
            avg_vol_3_month = cols[6].text
            market_cap = cols[7].text
            pe_ratio = cols[8].text
            data.append([symbol, name, last_price, change, percent_change, 
                         volume, avg_vol_3_month, market_cap, pe_ratio])

        # Create a pandas DataFrame from the extracted data.
        df = pd.DataFrame(data, columns=['Symbol', 'Name', 'Last Price', 'Change', 'Percent Change',
                                         'Volume', 'Avg Vol 3 Months', 'Market Cap', 'PE Ratio (TTM)'])
        return df
    else:
        print(f"Failed to retrieve data for page {page_number}. Status code: {response.status_code}")
        return None

# Initialize an empty DataFrame to store all the data.
combined_data = pd.DataFrame(columns=['Symbol', 'Name', 'Last Price', 'Change', 'Percent Change',
                                      'Volume', 'Avg Vol 3 Months', 'Market Cap', 'PE Ratio (TTM)'])

# Scrape the first page and add it to the combined_data DataFrame.
first_page = scrape_gainers_page(0)

if first_page is not None:
    if not combined_data.empty:
        # If the combined_data is not empty, use pd.concat
        combined_data = pd.concat([combined_data, first_page], ignore_index=True)
    else:
        # If the combined_data is empty, set it directly
        combined_data = first_page.copy()

# Scrape the next 10 pages and append the data to the combined_data DataFrame.
for page_number in range(1, 11):
    page_data = scrape_gainers_page(page_number)
    if page_data is not None:
        combined_data = pd.concat([combined_data, page_data], ignore_index=True)

# Save the combined data to a CSV file.
combined_data.to_csv("top_gainers_collected.csv", index=False)
