import sqlite3
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from flask import Flask, jsonify, request

app = Flask(__name__)

# ARIMA模型函數
def predict_bike_quantity(station_id, steps=10):
    conn = sqlite3.connect('youbike_data_test.db')
    
    # 提取指定站點的數據
    query = f"""
    SELECT fetch_time, available_rent_bikes
    FROM youbike_station_history
    WHERE sno = '{station_id}'
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    # 轉換 fetch_time 為日期時間格式，並設置為索引
    df['fetch_time'] = pd.to_datetime(df['fetch_time'])
    df.set_index('fetch_time', inplace=True)
    # 每分鐘收集資料
    df = df.asfreq('min')  

    # 構建並訓練 ARIMA 模型
    model = ARIMA(df['available_rent_bikes'], order=(5, 1, 0))
    model_fit = model.fit()

    # 預測未來steps步的數量
    forecast = model_fit.forecast(steps=steps)
    return forecast.tolist()  # 將結果轉為列表

# 定義API路由
@app.route('/predict', methods=['POST'])
def predict():
    # 確保以 JSON 格式解碼
    data = request.get_json(force=True)  
    print("Received data:", data) 
    station_id = next((item[1] for item in data if item[0] == "sno"), None)
    print("Station ID:", station_id)
    # 確保站點編號存在
    if not station_id:
        return jsonify({'error': 'station_id is required'}), 400

    # 獲取預測結果
    forecast = predict_bike_quantity(station_id)
    
    # 若無法預測則回傳錯誤
    if forecast is None:
        return jsonify({'error': 'No data available for the specified station'}), 404
    
    # 回傳預測結果
    print("Predicted quantities:", forecast)
    return jsonify({'station_id': station_id, 'predicted_quantities': forecast})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
