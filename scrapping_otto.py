# ==== IMPORT STATEMENTS ====

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
from functions import p_filter,p_cleaner,k_filter,s_cleaner



# ==== SCRAPPING OTTO.DE ====

def otto_scrapper(product,min_price,max_price,keywords):

    data = []

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option('detach', True)
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)



    # ==== OPENING OTTO.DE AND SEARCHING PRODUCT ===

    driver.get('https://www.otto.de')
    search_bar = wait.until(
        ec.element_to_be_clickable((By.XPATH, '//*[@id="js_squirrel_stomachshop"]/div/form/div/div/input')))
    search_bar.click()
    search_bar.send_keys(f'{product}', Keys.ENTER)



    # ==== ACCEPTING COOKIES ====

    cookies = wait.until(ec.presence_of_element_located((By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')))
    cookies.click()



    # ==== LOCATING ALL PRODUCTS ====

    wait.until(ec.presence_of_all_elements_located((By.CLASS_NAME, 'product')))
    all_products = driver.find_elements(By.CLASS_NAME, 'product')



    # ==== SCRAPPING INDIVIDUAL PRODUCTS INFORMATION ====

    for p in all_products:
        driver.execute_script("arguments[0].scrollIntoView();", p)  # SCROLLING THE PAGE
        wait.until(lambda d: p.find_element(By.CLASS_NAME, 'find_tile__productLink'))  # WAITING UNTIL PRODUCT IS LOADED

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

