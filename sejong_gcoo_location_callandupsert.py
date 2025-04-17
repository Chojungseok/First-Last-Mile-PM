import os
import requests
from dotenv import load_dotenv
from pprint import pprint
import psycopg2

load_dotenv()

url  = 'http://apis.data.go.kr/1613000/PersonalMobilityInfoService'
get_path = 'getPMListByProvider'

API_KEY = os.environ['API_KEY']
numOfRows = 2000
provider_name = 'GBIKE'
city_code = 12

payload = {
    'serviceKey': API_KEY,
    'numOfRows': numOfRows,
    'providerName': provider_name, 
    'cityCode': city_code,
    '_type': 'json'
}


requests_url = f'{url}/{get_path}'

res = requests.get(requests_url, params=payload)
res = res.json()
total_count = res['response']['body']['totalCount']
datas = res['response']['body']['items']['item']
pprint(datas[:5])



# postgresql 연결

# 데이터베이스 연결 설정
try:
    connection = psycopg2.connect(
        dbname="sejong",
        user="chojungseok",
        password="jungseok0324!",
        host="localhost",
        port="5432"
    )
    
    cursor = connection.cursor()

    upsert_query = """
        INSERT INTO GBIKE (battery, citycode, cityname, latitude, longitude, providername, vehicleid)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (vehicleid) DO UPDATE SET
            battery = EXCLUDED.battery,
            citycode = EXCLUDED.citycode,
            cityname = EXCLUDED.cityname,
            latitude = EXCLUDED.latitude,
            longitude = EXCLUDED.longitude,
            providername = EXCLUDED.providername;
    """

    for data in datas:
        cursor.execute(upsert_query, (
            data['battery'], data['citycode'], data['cityname'],
            data['latitude'], data['longitude'], data['providername'],
            data['vehicleid']
        ))

    connection.commit()

except Exception as error:
    print('error 발생', error)

finally:
    if connection:
        cursor.close()
        connection.close()
        print("Connection closed.")

