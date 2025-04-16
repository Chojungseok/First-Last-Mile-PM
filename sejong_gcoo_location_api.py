import os
import requests
from dotenv import load_dotenv
from pprint import pprint

load_dotenv()

url  = 'http://apis.data.go.kr/1613000/PersonalMobilityInfoService'
get_path = 'getPMListByProvider'

API_KEY = os.environ['API_KEY']
pageNo = 1500
provider_name = 'GBIKE'
city_code = 12

payload = {
    'serviceKey': API_KEY,
    'pageNo': pageNo,
    'providerName': provider_name, 
    'cityCode': city_code,
    '_type': 'json'
}


requests_url = f'{url}/{get_path}'

res = requests.get(requests_url, params=payload)
res = res.json()
total_count = res['response']['body']['totalCount']
# pprint(res['response']['body']['totalCount'])
# pprint(len(res['response']['body']['items']['item']))

