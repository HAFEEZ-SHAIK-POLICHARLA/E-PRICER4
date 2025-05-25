# ==== IMPORT STATEMENTS ====

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
from functions import p_filter,p_cleaner,k_filter,s_cleaner,get_headless_driver



# ==== SCRAPING OTTO.DE ====

def otto_scraper(product,min_price,max_price,keywords):

    data = []

    driver = get_headless_driver()
    wait = WebDriverWait(driver, 10)



    # ==== OPENING OTTO.DE ====
    driver.get('https://www.otto.de')



    # === ACCEPT COOKIES ===
    try:
        cookies = wait.until(ec.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler')))
        driver.execute_script("arguments[0].click();", cookies)
    except:
        pass  



    # === SEARCH PRODUCT ===
    search_bar = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, "input[data-qa='ftfind-search-field']")))
    search_bar.send_keys(product, Keys.ENTER)



    # ==== LOCATING ALL PRODUCTS ====

    wait.until(ec.presence_of_all_elements_located((By.CLASS_NAME, 'product')))
    all_products = driver.find_elements(By.CLASS_NAME, 'product')



    # ==== SCRAPING INDIVIDUAL PRODUCTS INFORMATION ====

    for p in all_products:
        driver.execute_script("arguments[0].scrollIntoView();", p)  
        wait.until(lambda d: p.find_element(By.CLASS_NAME, 'find_tile__productLink'))  

        product_name_otto = p.find_element(By.CLASS_NAME, 'find_tile__productLink').get_attribute('title')
        clean_product_name_otto = s_cleaner(product_name_otto)

        product_url_otto = p.find_element(By.CLASS_NAME, 'find_tile__productLink').get_attribute('href')

        product_price_otto = p.find_element(By.CSS_SELECTOR,".find_tile__retailPrice.pl_headline50.find_tile__priceValue").text
        clean_product_price_otto = p_cleaner(product_price_otto)



        # ==== FILTERING PRODUCT AND ADDING TO DATA ====

        if p_filter(clean_product_price_otto, min_price, max_price) == True and k_filter(keywords,product_name_otto) == True:

            data.append({
                'Website': 'otto.de',
                'Name/Description': clean_product_name_otto,
                'Price': clean_product_price_otto,
                'URL': product_url_otto
            })
    driver.quit()

    return data

