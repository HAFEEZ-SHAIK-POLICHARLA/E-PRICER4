# ==== IMPORT STATEMENTS ====

from scrapers.scraping_amazon import amazon_scraper
from scrapers.scraping_ebay import ebay_scraper
from scrapers.scraping_otto import otto_scraper
import pandas as pd
import streamlit as st



# ==== STYLING ====

st.markdown("""
    <style>
        /* Buttons */
        .stButton > button, .stDownloadButton > button {
            display: block;
            margin: 1rem auto;
            background-color: #f0c420;
            color: black;
            font-weight: bold;
            border: none;
            padding: 12px 26px;
            border-radius: 10px;
            font-size: 16px;
        }

        /* Centralize Buttons */
        div.stButton {
            display: flex;
            justify-content: center;
        }

        /* Subtitle */
        h2, h3 {
            text-align: center;
            color: #f0c420;
        }
    </style>
""", unsafe_allow_html=True)



# ==== TITLE ====

st.markdown(
    """
    <h1 style='text-align: center; color: #f0c420;'>Online Price Scraper</h1>
    <hr style="border:1px solid #CCC"/>
    """,
    unsafe_allow_html=True
)



# ==== HEADER AND START PAGE ====

if 'page' not in st.session_state:
    st.session_state.page = 'start'

if st.session_state.page == 'start':
    if st.button('start'):
        st.session_state.page = 'scraper'




# ==== SCRAPER PAGE ====

if st.session_state.page == 'scraper':
    st.warning('Google Chrome is necessary to load the scraper. Make sure you have it installed')


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

        product = st.session_state.get("product", "").strip()
        min_price = st.session_state.get("min_price", None)
        max_price = st.session_state.get("max_price", None)
        k_list = st.session_state.get("k_list", None)

        if not product:
            st.error("Please enter a product name.")

        elif min_price is None or max_price is None:
            st.error("Please enter both minimum and maximum price.")

        elif k_list is None:
            st.error("Please provide a keyword list or choose 'No'.")

        else:

            st.success("The scraper will sucessfully start.")


            # ==== MERGING DATA ====

            data = []
            
            with st.spinner("Scraping in progress... please wait and make sure to have a stable internet connection."):
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
                label='Download csv',
                data=df.to_csv(index=False).encode('utf-8'),
                file_name='products.csv',
                mime='text/csv'
                )
                st.session_state.scraping_finished = True  


    if st.session_state.get("scraping_finished", False):
        if st.button('Next'):
            st.session_state.page = 'edit_data'
            st.rerun()
                
    
            


# ==== DATA EDITOR PAGE ====

if st.session_state.page == 'edit_data':
    st.markdown("<h2>Edit and Filter Scraped Data</h2>", unsafe_allow_html=True)


    # === LOAD DATA ===

    st.session_state.df = pd.read_csv("products.csv")
    df = st.session_state.df


    # === FILTERS ===

    selected_site = st.selectbox("Filter by website:", options=sorted(df["Website"].unique()))
    min_price = st.number_input("Minimum price:", value=float(df["Price"].min()))
    max_price = st.number_input("Maximum price:", value=float(df["Price"].max()))

    filtered_df = df[
        (df["Website"] == selected_site) &
        (df["Price"] >= min_price) &
        (df["Price"] <= max_price)
    ].sort_values(by="Price").reset_index(drop=True)


    # === TABLE ===

    edited_df = st.data_editor(filtered_df, use_container_width=True, num_rows="dynamic")


    # === SAVE EDITED DATA ===

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


    # === DOWNLOAD EDITED VERSION ===

    csv_filtered = edited_df.to_csv(index=False).encode("utf-8")
    st.download_button("Download filtered CSV", csv_filtered, "filtered_products.csv", "text/csv")


    # === NAVIGATION ===

    if st.button("Back"):
        st.session_state.page = 'scraper'
        st.rerun()