# ==== IMPORT STATEMENTS ====

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
from functions import p_filter,p_cleaner,k_filter,s_cleaner



# ==== SCRAPING EBAY.DE ====

def ebay_scraper(product,min_price,max_price,keywords):

    data = []

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option('detach', True)
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 15)
    driver.get('https://www.ebay.de')



    # ==== ACCEPTING COOKIES ===

    cookies = wait.until(ec.element_to_be_clickable((By.ID,'gdpr-banner-accept')))
    driver.execute_script("arguments[0].click();", cookies)



    # ==== SEARCHING PRODUCT ===

    search_bar = driver.find_element(By.CSS_SELECTOR,'.gh-search-input.gh-tb.ui-autocomplete-input')
    search_bar.click()
    search_bar.send_keys(f'{product}',Keys.ENTER)
    all_products = wait.until(ec.presence_of_all_elements_located((By.CSS_SELECTOR,'.s-item.s-item__dsa-on-bottom.s-item__pl-on-bottom')))



    # ==== SCRAPING INDIVIDUAL PRODUCTS INFORMATION ===

    for p in all_products:
        driver.execute_script("arguments[0].scrollIntoView();", p)  # SCROLLING THE PAGE
        wait.until(lambda d: p.find_element(By.CSS_SELECTOR, '.s-item__link'))

        product_url_ebay = p.find_element(By.CLASS_NAME,'s-item__link').get_attribute('href')

        product_name_ebay = p.find_element(By.CSS_SELECTOR,'.s-item__title [role="heading"]').text
        clean_product_name_ebay = s_cleaner(product_name_ebay)

        product_price_ebay = p.find_element(By.CSS_SELECTOR,'.s-item__price .ITALIC').text
        clean_product_price_ebay = p_cleaner(product_price_ebay)



        # ==== FILTERING PRODUCT AND ADDING TO DATA ====

        if p_filter(clean_product_price_ebay, min_price, max_price) == True and k_filter(keywords,clean_product_name_ebay) == True:

            data.append({
                'Website': 'ebay.de',
                'Name/Description': clean_product_name_ebay,
                'Price': clean_product_price_ebay,
                'URL': product_url_ebay
            })
    driver.quit()

    return data

