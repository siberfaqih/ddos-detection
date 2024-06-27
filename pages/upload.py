import streamlit as st
import pandas as pd
import numpy as np
from streamlit_option_menu import option_menu
from sklearn.preprocessing import StandardScaler
import joblib
from menu import menu_with_redirect

menu_with_redirect()

# Load trained model and scaler
model = joblib.load('pages/rf.pkl')  # Replace with your model file name
scaler = joblib.load('pages/scaler.pkl')  # Replace with your scaler file name



st.title('DDoS Detection Application')

uploaded_file = st.file_uploader("Upload CSV file (DDoS features)", type=['csv'])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)

        # Feature selection
        features = ['fwd_pkt_len_std', 'tot_bwd_pkts', 'totlen_bwd_pkts', 'fwd_act_data_pkts',
                    'bwd_iat_tot', 'bwd_pkt_len_mean', 'idle_mean', 'flow_iat_max']

        # Feature validation
        if all(feature in df.columns for feature in features):
            # Data scaling
            df_scaled = scaler.transform(df[features])

            # Prediction
            predictions = model.predict(df_scaled)

            # Map predictions to labels
            df['predictions'] = ['DDoS' if pred == 1 else 'Benign' for pred in predictions]

            # Display options
            num_rows_to_display = st.slider("Number of predictions to display:", 100, 1000, 100)

            # Display predictions
            st.subheader('Predictions Result')

            # Add color to predictions
            def color_predictions(val):
                color = 'red' if val == 'DDoS' else 'green'
                return f'background-color: {color}'

            df_display = df[['timestamp', 'src_ip', 'dst_ip'] + features + ['predictions']].head(num_rows_to_display)
            styled_df = df_display.style.applymap(color_predictions, subset=['predictions'])

            st.dataframe(styled_df)
            
            df_pred_counts = df['predictions'].value_counts().reset_index()
            st.dataframe(df_pred_counts.style.applymap(color_predictions, subset=['predictions']))
            

        else:
            st.warning(f"Required features {features} are not present in the uploaded file.")

    except Exception as e:
        st.error(f"An error occurred while processing the file: {e}")

else:
    st.info('Upload a CSV file containing DDoS features to begin.')
