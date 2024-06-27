import streamlit as st
import requests
import pandas as pd
import time
from menu import menu_with_redirect

menu_with_redirect()

API_URL = "http://localhost:8000/get_data"

def fetch_data():
    try:
        response = requests.get(API_URL)
        print(pd.json_normalize(response.json()))
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error: Received status code {response.status_code}")
            return None
    except requests.RequestException as e:
        st.error(f"Error fetching data: {e}")
        return None

def main():
    st.title("Analisis Lalu Lintas Jaringan Real-time")

    data_placeholder = st.empty()

    while True:
        data = fetch_data()
        if data:
            columns = ['timestamp', 'src_ip', 'dst_ip',
           'fwd_pkt_len_std', 'tot_bwd_pkts', 'totlen_bwd_pkts',
           'fwd_act_data_pkts', 'bwd_iat_tot', 'bwd_pkt_len_mean',
           'idle_mean', 'flow_iat_max', 'predictions']
            df = pd.DataFrame(data, columns=columns)
            def color_predictions(val):
                color = 'red' if val == 'DDoS' else 'green'
                return f'background-color: {color}'

            styled_df = df.style.map(color_predictions, subset=['predictions'])

            st.dataframe(styled_df)
            
            
        time.sleep(5)  # Perbarui setiap 5 detik

if __name__ == "__main__":
    main()