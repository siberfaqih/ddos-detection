from flask import Flask, request, jsonify
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import datetime

app = Flask(__name__)

# Simpan data dalam memori
data_store = []

# Asumsikan kita memiliki model yang sudah dilatih sebelumnya
# Ganti ini dengan model Anda sendiri
model = joblib.load('rf.pkl')
scaler = joblib.load('scaler.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
   
     # Define the features to be extracted from the JSON data
    features = ['fwd_pkt_len_std',
     'tot_bwd_pkts',
     'totlen_bwd_pkts',
     'fwd_act_data_pkts',
     'bwd_iat_tot',
     'bwd_pkt_len_mean',
     'idle_mean',
     'flow_iat_max'
     ]
  
    

    # Extract features and convert to numeric, defaulting to 0 if not found
    extracted_features = [data.get(feature, 0) for feature in features]

    df = pd.json_normalize(data)

    df_scale = scaler.transform(df[features])
    try:
        # Perform prediction
        prediction = model.predict(df_scale)
        # prediction = model.predict(df[features])[0]
    except Exception as e:
        print(f"Error during prediction: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

    # Convert prediction to label
    label = 'DDoS' if prediction == 1 else 'Benign'
    df['predictions'] = label
     
    data_store.append(df[['timestamp', 'src_ip', 'dst_ip'] + features + ['predictions']].to_dict(orient='records')[0])

    # Batasi penyimpanan data (misalnya, hanya simpan 1000 data terakhir)
    if len(data_store) > 1000:
        data_store.pop(0)
 
    # Return JSON response with IP and prediction
    return jsonify({'IP': data.get('src_ip', 0), 'prediction': label}) 


@app.route('/get_data', methods=['GET'])
def get_data():
    # Endpoint ini akan digunakan oleh Streamlit untuk mengambil data
    return jsonify(data_store)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)