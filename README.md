# Group_5_Project_Intro_to_Python
DAB111-004: Group Project

Students: 



Rodrigo Paz Ramirez

## Project/Goals
1. Develop a website capable of autonomously updating information on the top 250 gainers in the financial market.

2. Implement a reliable web scraping mechanism to extract relevant data from 'https://finance.yahoo.com/gainers.'

3. Perform thorough data processing, including cleaning, organizing, and transforming the scraped data into a structured format.

4. Store the processed data in an SQLite database for efficient retrieval and management.

5. Establish periodic web scraping routines to ensure the information on the website remains accurate and up-to-date.

6. Provide users with a dynamic and interactive experience by integrating the website with the processed data stored in the SQLite database.
   
8. Implement real-time plot updates to visually represent changes in the top gainers, and allow users to explore more accurate and precise data by providing the option to view information on a per-company basis. This feature enhances the user's ability to analyze individual companies within the financial market dynamically.


## Process
### Data Collection
1. URL Access:
   * Identify the URL of the webpage containing the desired data. In this case, it's 'https://finance.yahoo.com/gainers,' which lists the top gainers in the financial market.
2. HTTP Request:
   * Use Python, along with a web scraping library such as BeautifulSoup.
3. HTML Parsing:
   * Retrieve the HTML content of the webpage as a response. Parse this HTML content to extract relevant information using BeatifulSoup
4. Data Extraction:
    * Identify the HTML elements that contain the data you need, such as Symbol, Name, Last Price, Change, Percent Change,                         Volume, Avg Vol 3 Months, Market Cap, PE Ratio (TTM).

### Data Processing
1. Percentage Conversion:
    * Transform percentage values by removing the '%' sign and converting them into decimal form. For example, '+16.13%' becomes '0.1613' and '-03.76%' becomes '-0.0376'.
2. Volume, Avg Vol 3 Months, Market Cap Formatting:
    * Format numerical values by converting abbreviations such as 'B' (billion) to their numeric equivalents. For example, '4.56B' becomes '4,560'000,000'. Apply this formatting to columns like Volume, Avg Vol 3 Months, and Market Cap.
3. Handling NaN Values:
    * Identify and handle blank spaces in the DataFrame, which represent NaN values. In this case, if there are rows with missing information denoted by blank spaces in the Volume, Avg Vol 3 Months, and Market Cap columns, remove those rows. This step ensures that the dataset is free of incomplete or ambiguous data, creating a cleaner and more reliable dataset for analysis.
4. Time Indicator Column:
    * Add a new column to the dataset that represents the timestamp or date of the data. This column could be in the 'yyyy/mm/dd' format, indicating the year, month, and day when the data was collected. This time indicator column provides a reference point for when each set of data was recorded.
5. 
### Database


### Website

## Results
(fill in what you discovered this data could tell you and how you used the data to answer those questions)

## Challenges 
(discuss challenges you faced in the project)

## Future Goals
(what would you do if you had more time?)
