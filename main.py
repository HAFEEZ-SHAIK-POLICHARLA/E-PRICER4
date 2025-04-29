# ==== IMPORT STATEMENTS ====

from scrapers.scraping_amazon import amazon_scraper
from scrapers.scraping_ebay import ebay_scraper
from scrapers.scraping_otto import otto_scraper
import pandas as pd


# ==== VARIABLES ===

max_price = None
min_price = None
k_list = None



# ==== PRODUCT NAME INPUT ====

while True:
    product = input("Please type a product of your choice.\nProduct name:\n")
    if product.strip():
        break
    print('Please type a valid string. For example: Iphone 13')



# ==== PRICE FILTER INPUT ====

while True:
    price_filter = input("Would you like to set a price filter?\nType n or y:\n").lower()

    if price_filter == 'y':
        while True:
            try:
                max_price = float(input('What would be the maximum price?:\n'))
                min_price = float(input('What would be the minimum price?:\n'))
                break
            except ValueError:
                print('Please enter a valid number using digits and optionally a dot. For example: 99.99')
        break

    elif price_filter == 'n':
        max_price = 'unlimited'
        min_price = 'unlimited'
        break

    else:
        print('Please type either y or n. Try again.')



# ==== KEYWORD FILTER INPUT ====

while True:
    keyword_filter = input("Would you like to set a keyword filter?\nType n or y:\n").lower()

    if keyword_filter == 'y':
        while True:
            keywords_string = input('Type the keywords (separated by commas) you would like to filter in:\n')
            k_list = [word.strip().lower() for word in keywords_string.split(',') if word.strip()]

            if k_list:
                break
            print('Please write at least one valid keyword.\nFor example: Pro, Max, Case')
        break

    elif keyword_filter == 'n':
        k_list = "empty"
        break

    else:
        print('Please type either y or n. Try again.')



# ==== MERGING DATA ====

data = []

for scraper in [otto_scraper, amazon_scraper, ebay_scraper]:
    result = scraper(product, min_price, max_price, k_list)
    if result:
        data.extend(result)

df = pd.DataFrame(data)
df.to_csv("products.csv", index=False)



# ==== INSTRUCTIONS FOR COLAB NOTEBOOK ===

print('\nYour data has been saved to "products.csv".')
print('You can now manipulate your product data in Google Colab or in Excel.')
print(f'To use Google Colab, open the "Notebook_PCT.ipnyb"')
print('2. Run the first cell to upload the CSV file when prompted.')
print('3. Use the other cells to filter, sort, and analyze your product table.')
print('Alternatively, just open the CSV in Excel or Google Sheets.')