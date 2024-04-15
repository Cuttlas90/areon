import requests
import streamlit as st


@st.cache_data(ttl=600)
def areon_query(queryString):
    url = 'https://areon-api.cuttlas.app/user/runQuery'
    myobj = {'queryString': queryString}

    x = requests.post(url, json = myobj).json()
    return x["data"]["result"]


