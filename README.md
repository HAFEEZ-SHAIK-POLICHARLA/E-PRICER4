# Online Price Scraper

Online Price Scraper is a Python web application that allows users to search, filter, edit, and download product data from Amazon, eBay, and Otto.de.

It uses Selenium to scrape product information and Streamlit to provide a interface.

---

## Features

- Search products by name
- Filter by price range
- Optional keyword filtering
- View and edit scraped data in-app
- Download full or filtered results as CSV
- UI

## How to Use

1. Clone the repository:

   ```bash
   git clone https://github.com/Andradeg271/products-price-scraper.git
   cd products-price-scraper
   ```

2. Run the application:

   ```bash
   streamlit run main.py
   ```

3. A browser tab will open automatically with the app interface.

4. Enter the name of the product you're looking for.

5. Set a minimum and maximum price range.

6. Optionally, provide keywords to narrow down your search.

7. Click the **Scrap** button to start the scraping process.

8. Wait a few seconds while data is collected from Amazon, eBay, and Otto.

9. Download the full results if needed, or click **Next** to edit/filter them.

10. After editing, you can save and download the updated list as a CSV file.

---

## Notes

- This app must be run locally. It will not work on Streamlit Cloud due to Selenium and ChromeDriver limitations.
- Scraping may break if the structure of the target websites changes.
- Make sure Google Chrome and the matching version of ChromeDriver are installed and accessible in your system path.
- Make sure you have a stable internet connection

---
