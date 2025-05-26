# ==== IMPORT STATEMENTS ====

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
from functions import p_filter,p_cleaner,k_filter,s_cleaner,get_headless_driver
from selenium.common.exceptions import NoSuchElementException



# ==== SCRAPING AMAZON.DE ====

def amazon_scraper(product,min_price,max_price,keywords):

    data = []


    driver = get_headless_driver()
    wait = WebDriverWait(driver, 35)
    driver.get('https://www.amazon.de')



    # ==== ACCEPTING COOKIES ====

    try:
        cookies = wait.until(ec.element_to_be_clickable((By.ID, 'sp-cc-accept')))
        cookies.click()
    except:
        pass  



    # ==== LOCATING ALL PRODUCTS ====

    try:
        search_bar = wait.until(ec.element_to_be_clickable((By.ID, "twotabsearchtextbox")))
        search_bar.send_keys(product, Keys.ENTER)

        try:
            search_for = wait.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="a-autoid-0-announce"]/span[1]')))
            search_for.click()
            best_seller = wait.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="s-result-sort-select_5"]')))
            best_seller.click()
        except:
            pass  

        all_products = wait.until(ec.presence_of_all_elements_located((By.CSS_SELECTOR, '[role="listitem"]')))
    except:
        driver.quit()
        return []



    # ==== SCRAPING INDIVIDUAL PRODUCTS INFORMATION ====

    for p in all_products:
        driver.execute_script("arguments[0].scrollIntoView();", p)  # SCROLLING THE PAGE
        wait.until(lambda d: p.find_element(By.CSS_SELECTOR, '.a-link-normal.s-line-clamp-2.s-link-style.a-text-normal'))

        product_url_amazon = p.find_element(By.CSS_SELECTOR,'.a-link-normal.s-line-clamp-2.s-link-style.a-text-normal').get_attribute('href')
        print(product_url_amazon)

        product_name = p.find_element(By.CSS_SELECTOR, 'h2[aria-label]').get_attribute('aria-label')
        clean_product_name_amazon = s_cleaner(product_name)
        print(clean_product_name_amazon)



        # ==== CHECKING IF PRICE IS LISTED (AMAZON HIDES SOME PRICES) ====

        try:
            product_price = p.find_element(By.CSS_SELECTOR,'.a-price .a-price-whole').text
            clean_product_price_amazon = p_cleaner(product_price)



            # ==== IF PRICE IS LISTED -> FILTERING PRODUCT AND ADDING TO DATA ====

            if p_filter(clean_product_price_amazon,min_price,max_price) == True and k_filter(keywords,clean_product_name_amazon) == True:

                data.append({
                    'Website': 'amazon.de',
                    'Name/Description': clean_product_name_amazon,
                    'Price': clean_product_price_amazon,
                    'URL': product_url_amazon
                })
        except NoSuchElementException:
            continue

    driver.quit()

    return data