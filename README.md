# Group_5_Project_Intro_to_Python
DAB111-004: Group Project

Students: 

Navjot Kaur

Pawan Kumar
Sandeep Sandeep
Rodrigo Paz Ramirez

## Project/Goals
1. Develop a website capable of autonomously updating information on the top 250 gainers in the financial market.

2. Implement a reliable web scraping mechanism to extract relevant data from [Yahoo Finance Top Gainers](https://finance.yahoo.com/gainers.)

3. Perform thorough data processing, including cleaning, organizing, and transforming the scraped data into a structured format.

4. Store the processed data in an SQLite database for efficient retrieval and management.

5. Establish periodic web scraping routines to ensure the information on the website remains accurate and up-to-date.

6. Provide users with a dynamic and interactive experience by integrating the website with the processed data stored in the SQLite database.
   
8. Implement real-time plot updates to visually represent changes in the top gainers, and allow users to explore more accurate and precise data by providing the option to view information on a per-company basis. This feature enhances the user's ability to analyze individual companies within the financial market dynamically.


# Process
## Data Collection
1. URL Access:
   * Identify the URL of the webpage containing the desired data. In this case, it's 'https://finance.yahoo.com/gainers,' which lists the top gainers in the financial market.
2. HTTP Request:
   * Use Python, along with a web scraping library such as BeautifulSoup.
3. HTML Parsing:
   * Retrieve the HTML content of the webpage as a response. Parse this HTML content to extract relevant information using BeatifulSoup
4. Data Extraction:
    * Identify the HTML elements that contain the data you need, such as Symbol, Name, Last Price, Change, Percent Change,                         Volume, Avg Vol 3 Months, Market Cap, PE Ratio (TTM).

## Data Processing
1. Percentage Conversion:
    * Transform percentage values by removing the '%' sign and converting them into decimal form. For example, '+16.13%' becomes '0.1613' and '-03.76%' becomes '-0.0376'.
2. Volume, Avg Vol 3 Months, Market Cap Formatting:
    * Format numerical values by converting abbreviations such as 'B' (billion) to their numeric equivalents. For example, '4.56B' becomes '4,560'000,000'. Apply this formatting to columns like Volume, Avg Vol 3 Months, and Market Cap.
3. Handling NaN Values:
    * Identify and handle blank spaces in the DataFrame, which represent NaN values. In this case, if there are rows with missing information denoted by blank spaces in the Volume, Avg Vol 3 Months, and Market Cap columns, remove those rows. This step ensures that the dataset is free of incomplete or ambiguous data, creating a cleaner and more reliable dataset for analysis.
4. Time Indicator Column:
    * Add a new column to the dataset that represents the timestamp or date of the data. This column could be in the 'yyyy/mm/dd' format, indicating the year, month, and day when the data was collected. This time indicator column provides a reference point for when each set of data was recorded.
5. Grouping by Company:
      * Group the main DataFrame by the 'Company' column. This will create separate groups, each corresponding to a unique company.
6. Iterating Through Groups:
      * Iterate through each group and create a new DataFrame for each company.
7. Saving as CSV:
      * For each company DataFrame, save it as a CSV file, where the filename could be based on the company name or a unique identifier.
8. Scheduled CSV Update:
      * Implement a function that includes the steps to update and save the CSV files. Then, schedule this function to run at regular intervals of 2 min.
## Database

1. Store each of the csv's in databases for each company.
2. If you click on the database file it won't open until you transform the information back to a dataframe to start working with it.


## Website

This website is a Flask web application that visualizes data from the stock market from Yahoo Finance Top gainers companies . updates itself every 2 minutes following a specific schedule from 10:00 to 16:00 in weekdays when the stock market is open.

It has three main pages,

### Home Page:
Where you can select the company an the feature you want.

### About Page
 The about page gives you an explanation about how the website works.

### Visualization Page
Where it can be seen one of this features for each company (Last Price, Volume, Change, Percent Change and Market Cap). Also when you are in the visualization page you can select another features for the same company and the last update time when the data was updated.
If you have been watching a plot for a long time a not noticing any change in the plot, please refresh the page, sometimes the server has too many requests so it is difficult to manage all of them at the same time.

# Description:
## Last Price
Data that helps to track the recent performance of a stock and make informed decisions based on its current market value. It represents the most recent transaction price at which the stock was bought or sold.
## Volume
Total number of shares of a security (such as a stock) that have been traded during a specific period of time, typically over a trading day. It is a measure of market activity and liquidity, providing insights into the level of interest and participation in a particular stock.

## Change
Difference in the price from the initial value in the day. Positive difference change indicates an increase in value, while negative difference change indicates a decrease.

## Percent Change
Indicate the magnitude of the price movement relative to the starting point. Positive percentage change indicates an increase in value, while negative percentage change indicates a decrease. This feature is more used then only change because it gives an adimensional parameter to compare against other companies.


## Market Cap
It is a measure of the total value of a publicly traded company's outstanding shares of stock. It is calculated by multiplying the current market price of one share by the total number of outstanding shares. Market cap is a key indicator used by investors to assess the size and relative value of a company in the financial markets.


## Results
(fill in what you discovered this data could tell you and how you used the data to answer those questions)

## Challenges 
### Data Collection
1. Go across many pages to reach all the data upto the tenth page.
2. Find the html table indicators to reach the information needed.

### Data Processing
1. Blank Spaces Management
2. Transform summarized values as 4.6B to 4,600'000,000 to make it usable.
3. Transform the percentage string to a usable parameter, p.e. +19.83% to 0.1983
4. Round all the decimals to only two decimals for an easier visualization. 

### Data to Dataframes
1. This process was done to separate the information per company because the scrapped data was a dataframe where each row was a different company. So, it was needed to save each row in their respective csv file with the format name: {company_symbol}_data.csv
2. Add the updated scrapped data to each csv or create a new one if a company were not in the csv folder before.
3. Erase all the duplicated rows so the data that was readded accidentaly could be deleted. 

### Dataframes to Databases
1. Convert each csv into a database usable for the webpage

### Website
1. Create a website that let you choose the company and the feature you want to see.
2. When you go to the respective visualization then you can choose another feature from the same company only, if you want to see another company then you have to return to the home page.
3. Show the current time and then the last update time.


## Future Goals
1. Make the page update by itself intead of pressing F5 to show the updated data.
2. Not only scrap top gainers companies, also top losers or any other category in the stock market.
3. Make it look at the original website ([Yahoo Finance Top Gainers](https://finance.yahoo.com/gainers.)), showing only the Today's Top Gainers Companies by erasing the database at the opening of the market.

















