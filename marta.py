import requests
import json

query = {'apikey': '7c82f5d4-54bf-43a8-b687-63111af3f923'}
r = requests.get('http://developer.itsmarta.com/RealtimeTrain/RestServiceNextTrain/GetRealtimeArrivals', params=query)

result_json = json.loads(r.text)

# print result_json

parsed_result = [x  for x in result_json if x['DESTINATION'] == 'Airport' and x['STATION'] == 'COLLEGE PARK STATION']

print parsed_result

