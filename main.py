# ==== IMPORT STATEMENTS ====

from scrapers.scraping_amazon import amazon_scraper
from scrapers.scraping_ebay import ebay_scraper
from scrapers.scraping_otto import otto_scraper
import pandas as pd
import streamlit as st




# ==== HEADER AND START PAGE ====

st.title("Online Price Scraper")
if 'page' not in st.session_state:
    st.session_state.page = 'start'

if st.session_state.page == 'start':
    if st.button('start'):
        st.session_state.page == 'scraper'




# ==== SCRAPER PAGE ====

if st.session_state.page == 'scraper':
    


    # ==== PRODUCT NAME INPUT ====

    
    st.session_state.product = st.text_input("Please type a product of your choice.\nProduct name:\n")
    st.session_state.product.strip()



    # ==== PRICE FILTER INPUT ====
    

    st.session_state.max_price = st.number_input('What would be the maximum price?')
    st.session_state.min_price = st.number_input('What would be the minimum price?')



    # ==== KEYWORD FILTER INPUT ====


    st.session_state.keyword_filter = st.selectbox("Would you like to set a keyword filter?",["Yes","No"])

    if st.session_state.keyword_filter == 'Yes':
            st.session_state.keywords_string = st.text_input('Type the keywords (separated by commas) you would like to filter in')
            st.session_state.k_list = [word.strip().lower() for word in st.session_state.keywords_string.split(',') if word.strip()]

    elif st.session_state.keyword_filter == 'No':
        st.session_state.k_list = "empty"
        


    # ==== VALIDATION ====

    if st.button("Scrap"):

        if not all([
            st.session_state.get("product", "").strip(),
            st.session_state.get("min_price"),
            st.session_state.get("max_price"),
            st.session_state.get("k_list")
        ]):
            st.error("Please fill all the boxes to continue")

        else:

            st.success("The scraper will sucessfully start. Please wait and make sure you have google chrome installed.")


            # ==== MERGING DATA ====

            data = []

            for scraper in [otto_scraper, amazon_scraper, ebay_scraper]:
                result = scraper(
                    st.session_state.product,
                    st.session_state.min_price,
                    st.session_state.max_price,
                    st.session_state.k_list
                )
                if result:
                    data.extend(result)

            if not data:
                st.error("No result found with the selected filters.")
            else:
                df = pd.DataFrame(data)
                df.to_csv("products.csv", index=False)
                st.success("Products found and sucessfully saved.")
                st.download_button(
                    label= 'Download csv',
                    data = df,
                    file_name= 'products.csv',
                    mime = 'text/csv'
                    )
                if st.button('Next'):
                    st.session_state.page = 'edit_data'
    
            


# ==== DATA EDITOR PAGE ====

if st.session_state.page == 'edit_data':

    st.title("Edit and Filter Scraped Data")


    # === Load data ===

    st.session_state.df = pd.read_csv("products.csv")
    df = st.session_state.df


    # === Filters ===

    selected_site = st.selectbox("Filter by website:", options=sorted(df["Website"].unique()))
    min_price = st.number_input("Minimum price:", value=float(df["Price"].min()))
    max_price = st.number_input("Maximum price:", value=float(df["Price"].max()))

    filtered_df = df[
        (df["Website"] == selected_site) &
        (df["Price"] >= min_price) &
        (df["Price"] <= max_price)
    ].sort_values(by="Price").reset_index(drop=True)


    # === Editable table ===

    edited_df = st.data_editor(filtered_df, use_container_width=True, num_rows="dynamic")


    # === Save edited data ===

    if st.button("Save changes"):
        mask = (
            (df["Website"] == selected_site) &
            (df["Price"] >= min_price) &
            (df["Price"] <= max_price)
        )
        df.loc[mask] = edited_df.values
        st.session_state.df = df
        df.to_csv("products.csv", index=False)
        st.success("Changes saved successfully.")


    # === Download filtered version ===

    csv_filtered = edited_df.to_csv(index=False).encode("utf-8")
    st.download_button("Download filtered CSV", csv_filtered, "filtered_products.csv", "text/csv")


    # === Navigation ===

    if st.button("Back"):
        st.session_state.page = 'scraper'



# ==== INSTRUCTIONS FOR COLAB NOTEBOOK ===

print('\nYour data has been saved to "products.csv".')
print('You can now manipulate your product data in Google Colab or in Excel.')
print(f'To use Google Colab, open the "Notebook_PCT.ipnyb"')
print('2. Run the first cell to upload the CSV file when prompted.')
print('3. Use the other cells to filter, sort, and analyze your product table.')
print('Alternatively, just open the CSV in Excel or Google Sheets.')