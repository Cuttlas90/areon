"""Analytics page for Areon blockchain"""


import logging
import streamlit as st
import pandas as pd
import plotly.express as px
from request import areon_query
from slider import create_slider

st.set_page_config(layout='wide',
                   page_title="Areon Dashboard",
                    page_icon="./assets/favicon.ico",
                    initial_sidebar_state='expanded')

logging.basicConfig(filename='./log/example.log', level=logging.WARNING)

st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    .stDeployButton {
            visibility: hidden;
        }
    </style>
    """, unsafe_allow_html=True
)

with open('style.css', encoding="utf-8") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
st.sidebar.image(image="./assets/logo.png")
st.sidebar.header('Areon DashBoard `version 1`')


plot_height = st.sidebar.slider('Specify plot height', 200, 500, 250)

st.markdown('### Metrics')
col1, col2, col3 = st.columns(3)


# col1.metric("Peice", f"{ans['bitcoin']['usd']} $", f"{ans['bitcoin']['usd_24h_change']:.2f} %")

QUERY_STRING = "SELECT COUNT( DISTINCT hash) AS total_unique_hashes FROM transactions"
total_transactions = areon_query(QUERY_STRING)[0]["total_unique_hashes"]
col1.metric("Total No. of transaction", f"{total_transactions}")


QUERY_STRING = "SELECT COUNT( DISTINCT to_address) AS total_unique_to_addresses FROM transactions"
total_address = areon_query(QUERY_STRING)[0]["total_unique_to_addresses"]
col2.metric("Total No. of address", f"{total_address}")



QUERY_STRING = "SELECT MAX(number) AS biggest_block_number FROM blocks"
last_block = areon_query(QUERY_STRING)[0]["biggest_block_number"]
col3.metric("Last Block", f"{last_block}")

c1, c2 = st.columns(2)
with c1:
    st.markdown('### contracts deploy History')
    try:
        QUERY_STRING = """SELECT
                        DATE (blocks.timestamp) AS transaction_date,
                        COUNT(hash) AS daily_deploy_contracts
                        FROM
                        contracts
                        JOIN blocks ON contracts.block_number = blocks.number
                        GROUP BY
                        transaction_date
                        ORDER BY
                        transaction_date;"""
        contract_history = areon_query(QUERY_STRING)
        contract_history = pd.DataFrame(
            contract_history, columns=['transaction_date', "daily_deploy_contracts"])
        contract_history["daily_deploy_contracts"] = \
            contract_history["daily_deploy_contracts"].astype(int)
        contract_history['date_column'] = pd.to_datetime(
            contract_history['transaction_date'], format="%Y-%m-%d").dt.date
        contract_history_slider = create_slider(
            contract_history, "contract_history", "contract history range:")

        filtered_df = contract_history[contract_history['date_column'].between(
            contract_history_slider[0], contract_history_slider[1])]
        st.line_chart(
            filtered_df, x = 'date_column', y = "daily_deploy_contracts", height = plot_height)
    except Exception as e:
        st.write("not available now")
        logging.error("An unknown error occurred: %s", str(e), exc_info=True)
with c2:
    st.markdown('### tokens deploy History')
    try:
        QUERY_STRING = """blocks
                    transactions
                    Areon Workbench
                    Areon Dashboard
                    SELECT
                    DATE (blocks.timestamp) AS transaction_date,
                    COUNT(hash) AS daily_deploy_tokens
                    FROM
                    tokens
                    JOIN blocks ON tokens.block_number = blocks.number
                    GROUP BY
                    transaction_date
                    ORDER BY
                    transaction_date;
                    Format Query Run Query
                    """
        token_history = areon_query(QUERY_STRING)
        token_history = pd.DataFrame(token_history, columns=\
                                     ['transaction_date', "daily_deploy_tokens"])
        token_history["daily_deploy_tokens"] = token_history["daily_deploy_tokens"].astype(int)
        token_history['date_column'] = pd.to_datetime(
            token_history['transaction_date'], format="%Y-%m-%d").dt.date
        token_history_slider = create_slider(
            token_history, "token_history", "tokens history range:")

        filtered_df = token_history[token_history['date_column'].between(
            token_history_slider[0], token_history_slider[1])]
        st.line_chart(
            filtered_df, x = 'date_column', y = "daily_deploy_tokens", height = plot_height)
    except Exception as e:
        st.write("not available now")
        logging.error("An unknown error occurred: %s", str(e), exc_info=True)

c1, c2 = st.columns(2)
with c1:

    st.markdown('### Transaction History')
    try:
        QUERY_STRING = """blocks
                    transactions
                    Areon Workbench
                    Areon Dashboard
                    SELECT
                    DATE (block_timestamp) AS transaction_date,
                    COUNT(hash) AS daily_transaction_count
                    FROM
                    transactions
                    GROUP BY
                    transaction_date
                    ORDER BY
                    transaction_date
                    Format Query Run Query
                    """
        transaction_history = areon_query(QUERY_STRING)
        transaction_history = pd.DataFrame(
            transaction_history, columns=['transaction_date', "daily_transaction_count"])
        transaction_history["daily_transaction_count"] = \
            transaction_history["daily_transaction_count"].astype(int)
        transaction_history['date_column'] = pd.to_datetime(
            transaction_history['transaction_date'], format="%Y-%m-%d").dt.date
        transaction_history_slider = create_slider(
            transaction_history, "transaction_history", "transaction history range:")

        filtered_df = transaction_history[transaction_history['date_column'].between(
            transaction_history_slider[0], transaction_history_slider[1])]
        st.line_chart(
            filtered_df, x = 'date_column', y = "daily_transaction_count", height = plot_height)
    except Exception as e:
        st.write("not available now")
        logging.error("An unknown error occurred: %s", str(e), exc_info=True)
with c2:
    st.markdown('### Daily Active Address History')
    try:
        QUERY_STRING = """blocks
                    transactions
                    Areon Workbench
                    Areon Dashboard
                    SELECT
                    DATE (block_timestamp) AS transaction_date,
                    COUNT(DISTINCT from_address) AS daily_active_address
                    FROM
                    transactions
                    GROUP BY
                    transaction_date
                    ORDER BY
                    transaction_date
                    Format Query Run Query
                    """
        daily_active_address_history = areon_query(QUERY_STRING)
        daily_active_address_history = pd.DataFrame(
            daily_active_address_history, columns=['transaction_date', "daily_active_address"])
        daily_active_address_history["daily_active_address"] = \
            daily_active_address_history["daily_active_address"].astype(int)
        daily_active_address_history['date_column'] = pd.to_datetime(
            daily_active_address_history['transaction_date'], format="%Y-%m-%d").dt.date
        daily_active_address_slider = create_slider(
            daily_active_address_history,
            "daily_active_address_history",
            "daily active address history range:"
            )

        filtered_df = \
            daily_active_address_history[daily_active_address_history['date_column'].between(
            daily_active_address_slider[0], daily_active_address_slider[1])]
        st.line_chart(
            filtered_df, x = 'date_column', y = "daily_active_address", height = plot_height)
    except Exception as e:
        st.write("not available now")
        logging.error("An unknown error occurred: %s", str(e), exc_info=True)

# Row C

c1, c2 = st.columns(2)
with c1:
    st.markdown('### Daily Transactions Value History')
    try:
        QUERY_STRING = """SELECT
                    DATE (block_timestamp) AS transaction_date,
                    SUM(value) AS daily_eth_number_circulate
                    FROM
                    transactions
                    GROUP BY
                    transaction_date
                    ORDER BY
                    transaction_date"""
        daily_transaction_value_history = areon_query(QUERY_STRING)
        daily_transaction_value_history = pd.DataFrame(
            daily_transaction_value_history, columns=\
                ['transaction_date', "daily_eth_number_circulate"])
        daily_transaction_value_history["daily_eth_number_circulate"] = \
            daily_transaction_value_history["daily_eth_number_circulate"].astype(float)
        daily_transaction_value_history['date_column'] = pd.to_datetime(
            daily_transaction_value_history['transaction_date'], format="%Y-%m-%d").dt.date
        daily_transaction_value_slider = create_slider(
            daily_transaction_value_history,
            "daily_transaction_value_history",
            "daily transactions value history range:"
            )

        filtered_df = \
            daily_transaction_value_history[daily_transaction_value_history['date_column'].between(
            daily_transaction_value_slider[0], daily_transaction_value_slider[1])]
        st.line_chart(
            filtered_df, x = 'date_column', y = "daily_eth_number_circulate", height = plot_height)
    except Exception as e:
        st.write("not available now")
        logging.error("An unknown error occurred: %s", str(e), exc_info=True)

with c2:
    st.markdown('### Daily New Address History')
    try:
        QUERY_STRING = """WITH FirstDayTransactions AS (
                        SELECT
                            from_address,
                            MIN(DATE(block_timestamp)) AS first_appearance_date
                        FROM
                            transactions
                        GROUP BY
                            from_address
                        )

                        SELECT
                        first_appearance_date,
                        COUNT(*) AS new_from_addresses
                        FROM
                        FirstDayTransactions
                        GROUP BY
                        first_appearance_date
                        ORDER BY
                        first_appearance_date"""
        daily_new_address_history = areon_query(QUERY_STRING)
        daily_new_address_history = pd.DataFrame(
            daily_new_address_history, columns=['first_appearance_date', "new_from_addresses"])
        daily_new_address_history["new_from_addresses"] = \
            daily_new_address_history["new_from_addresses"].astype(int)
        daily_new_address_history['date_column'] = pd.to_datetime(
            daily_new_address_history['first_appearance_date'], format="%Y-%m-%d").dt.date
        daily_new_address_slider = create_slider(
            daily_new_address_history,
            "daily_new_address_history",
            "daily new address history range:"
            )


        filtered_df = daily_new_address_history[daily_new_address_history['date_column'].between(
            daily_new_address_slider[0], daily_new_address_slider[1])]
        st.line_chart(
            filtered_df, x = 'date_column', y = "new_from_addresses", height = plot_height)
    except Exception as e:
        st.write("not available now")
        logging.error("An unknown error occurred: %s", str(e), exc_info=True)

# Row D
c1, c2 = st.columns(2)
with c1:
    st.markdown('### Daily Paid Gas History')
    try:
        QUERY_STRING = """blocks
                    transactions
                    Areon Workbench
                    Areon Dashboard
                    SELECT
                    DATE (block_timestamp) AS transaction_date,
                    SUM(gas) AS daily_gas_paid
                    FROM
                    transactions
                    GROUP BY
                    transaction_date
                    ORDER BY
                    transaction_date;
                    Format Query Run Query
                    """
        daily_gas_paid_history = areon_query(QUERY_STRING)
        daily_gas_paid_history = pd.DataFrame(
            daily_gas_paid_history, columns=['transaction_date', "daily_gas_paid"])
        daily_gas_paid_history["daily_gas_paid"] = \
            daily_gas_paid_history["daily_gas_paid"].astype(int)
        daily_gas_paid_history['date_column'] = pd.to_datetime(
            daily_gas_paid_history['transaction_date'], format="%Y-%m-%d").dt.date
        daily_new_address_slider = create_slider(
            daily_gas_paid_history, "daily_gas_paid_history", "daily paid gas history range:")


        filtered_df = daily_gas_paid_history[daily_gas_paid_history['date_column'].between(
            daily_new_address_slider[0], daily_new_address_slider[1])]
        st.line_chart(filtered_df, x = 'date_column', y = "daily_gas_paid", height = plot_height)
    except Exception as e:
        st.write("not available now")
        logging.error("An unknown error occurred: %s", str(e), exc_info=True)

with c2:
    st.markdown('### Miners Share')
    try:
        QUERY_STRING = """SELECT miner, COUNT(*) AS block_count
                        FROM blocks
                        GROUP BY miner;"""
        miners_share = areon_query(QUERY_STRING)
        miners_share = pd.DataFrame(miners_share, columns=['miner', "block_count"])
        miners_share["block_count"] = miners_share["block_count"].astype(int)

        fig = px.pie(miners_share, names="miner",
                        values='block_count', height=300, width=200)
        fig.update_layout(margin=dict(l=20, r=20, t=30, b=0),)
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.write("not available now")
        logging.error("An unknown error occurred: %s", str(e), exc_info=True)

st.sidebar.markdown('''
---
Created with ❤️ by [Cuttlas Team](https://cuttlas.app).
''')
