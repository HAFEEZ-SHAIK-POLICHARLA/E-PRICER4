
# ==== PRICE CLEANER FUNCTION ====

def p_cleaner(price_str):
    clean_price = price_str.replace("€","").replace("$","").replace(".","").replace(",",".").replace("EUR","").replace("R$","").strip()
    return float(clean_price)



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



# ==== KEYWORDS FILTERING FUNCTION

def k_filter(keywords,p_name):
    if keywords == 'empty':
        return True
    else:
        for w in keywords:
            if w in p_name.lower():
                return True
        return False
