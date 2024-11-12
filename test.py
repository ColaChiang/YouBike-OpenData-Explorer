import sqlite3
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from flask import Flask, jsonify, request

app = Flask(__name__)

# 定義API路由
@app.route('/connect_test', methods=['POST'])
def predict():
    # 確保以 JSON 格式解碼
    data = request.get_json(force=True)  
    print("Received data:", data) 
    station_id = next((item[1] for item in data if item[0] == "sno"), None)
    print("Station ID:", station_id)
    
    # 測試訊息回傳
    test_message = "This is a test response from the backend."
    return jsonify({'message': test_message, 'station_id': station_id})
