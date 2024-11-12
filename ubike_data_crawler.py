import sqlite3
from datetime import datetime
import urllib.request
import json
import time

def fetch_and_store_youbike_data():
    url = "https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json"
    
    try:
        # 抓取資料
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
        
        # 連接 SQLite 資料庫
        conn = sqlite3.connect("C:/Users/Tosti/Downloads/YouBike_Program/youbike_data_test.db")  # 儲存在本地端
        cursor = conn.cursor()

        # 創建表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS youbike_station_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sno TEXT,
            sna TEXT,
            sarea TEXT,
            mday TEXT,
            ar TEXT,
            sareaen TEXT,
            snaen TEXT,
            aren TEXT,
            act TEXT,
            srcUpdateTime TEXT,
            updateTime TEXT,
            infoTime TEXT,
            infoDate TEXT,
            total INTEGER,
            available_rent_bikes INTEGER,
            latitude REAL,
            longitude REAL,
            available_return_bikes INTEGER,
            fetch_time TIMESTAMP
        )
        ''')

        # 插入資料
        insert_sql = '''
        INSERT INTO youbike_station_history (
            sno, sna, sarea, mday, ar, sareaen, snaen, aren, act,
            srcUpdateTime, updateTime, infoTime, infoDate, total,
            available_rent_bikes, latitude, longitude, available_return_bikes, fetch_time
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        
        current_time = datetime.now()
        for station in data:
            cursor.execute(insert_sql, (
                station["sno"],
                station["sna"],
                station["sarea"],
                station["mday"],
                station["ar"],
                station["sareaen"],
                station["snaen"],
                station["aren"],
                station["act"],
                station["srcUpdateTime"],
                station["updateTime"],
                station["infoTime"],
                station["infoDate"],
                int(station["total"]),
                int(station["available_rent_bikes"]),
                float(station["latitude"]),
                float(station["longitude"]),
                int(station["available_return_bikes"]),
                current_time
            ))

        conn.commit()
        conn.close()

        print(f"Data stored successfully at {current_time}")
    
    except Exception as e:
        print(f"Error fetching or storing data: {e}")

# 持續每分鐘執行一次
while True:
    fetch_and_store_youbike_data()
    time.sleep(60)  # 每60秒執行一次
