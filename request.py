"""manage different requests"""

import requests
import streamlit as st


@st.cache_data(ttl=600)
def areon_query(query_string):
    """query a sql on areon database"""
    url = 'https://api.chainbench.xyz/user/runQuery'
    myobj = {'queryString': query_string}

    x = requests.post(url, json = myobj, timeout=60).json()
    return x["data"]["result"]
