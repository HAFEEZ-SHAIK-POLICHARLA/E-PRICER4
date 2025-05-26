
# ==== PRICE CLEANER FUNCTION ====

import re

def p_cleaner(price_string):
    match = re.search(r"[\d.,]+", price_string)
    if not match:
        return 0.0

    raw = match.group()

    parts = raw.split('.')
    if len(parts) > 2:
        raw = ''.join(parts[:-1]) + '.' + parts[-1]

    clean_price = raw.replace(',', '.')

    try:
        return float(clean_price)
    except:
        return 0.0





# ==== STRING CLEANER FUNCTION ====

def s_cleaner(string):
    clean_string = string.replace("®","").replace("-","").replace("™","").replace("|","").strip()
    return clean_string



# ==== PRICE FILTERING FUNCTION ====

def p_filter(p_price,p_min_price,p_max_price):
    if p_max_price == 'unlimited' and p_min_price == 'unlimited':
        return True
    else:
        if p_max_price >= p_price >= p_min_price:
            return True
        else:
            return False



# ==== KEYWORDS FILTERING FUNCTION ====

def k_filter(keywords,p_name):
    if keywords == 'empty':
        return True
    else:
        for w in keywords:
            if w in p_name.lower():
                return True
        return False



# === HEADLESS AND LIGHT DRIVER FUNCTION ==== 

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def get_headless_driver():
    options = Options()
    options.add_argument("--headless=new")  
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--window-size=1920x1080")

    return webdriver.Chrome(options=options)
