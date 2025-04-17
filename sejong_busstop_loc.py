import pandas as pd
import psycopg2


file_path = '/Users/chojungseok/Desktop/mini_project/data/'
file_name = '세종도시교통공사_버스정류장_시설현황_20210924.csv'
bus_stop = pd.read_csv(file_path + file_name)

bus_stop.drop('연번', axis=1, inplace=True)

try:
    connection = psycopg2.connect(
        dbname="sejong",
        user="chojungseok",
        password="jungseok0324!",
        host="localhost",
        port="5432"
    )

    cursor = connection.cursor()

    insert_query = """
        INSERT INTO bus_stop (route_no, route_id, busstop_no, busstop_id, busstop_name, latitude, longitude)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (busstop_id) DO UPDATE SET
            route_no = EXCLUDED.route_no,
            route_id = EXCLUDED.route_id,
            busstop_no = EXCLUDED.busstop_no,
            busstop_name = EXCLUDED.busstop_name,
            latitude = EXCLUDED.latitude,
            longitude = EXCLUDED.longitude;
    """

    for index, row in bus_stop.iterrows():
        cursor.execute(insert_query, (
            row['노선번호'],
            row['노선ID'],
            row['정류소번호'],
            row['정류소ID'],
            row['정류소명'],
            row['위도'],
            row['경도']
        ))
    
    connection.commit()
except Exception as error:
    print('error 발생:', error)

finally: 
    if connection:
        cursor.close()
        connection.close()
        print("✅ Connection closed.")
