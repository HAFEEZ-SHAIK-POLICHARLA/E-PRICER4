# Product Price Scraper

This project is a Python-based scraper that gathers product data from three major e-commerce websites: **Otto**, **Amazon**, and **eBay**.  
The user can define filters (such as price range and keywords), and the program returns a CSV file with relevant product names, prices, and URLs.
This program uses Selenium with Chrome. Please make sure Google Chrome is installed on your system.

## How it works

1. Run the Python script `main.py` in your local environment.
2. You will be asked:
   - What product you're looking for
   - Whether you want to set a price filter (minimum and maximum)
   - Whether you want to filter results by keywords
3. The program then searches Otto, Amazon, and eBay for matching products and saves the results to a CSV file named products.csv.
4. Once complete, open the .ipnyb file

## Exploring your data

In this notebook, you can:

- Upload the CSV file you just created
- Filter products by keyword or by price
- Sort results from cheapest to most expensive and vice versa
- Filter results by website (Otto, Amazon, or eBay)
- Export modified versions of the CSV

If you prefer, you can also just open the CSV file with Excel or another spreadsheet software.
