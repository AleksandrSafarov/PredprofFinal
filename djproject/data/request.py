import requests
import json
import psycopg2

url = 'https://dt.miet.ru/ppo_it_final'
headers = {
    'Content-Type': 'application/vnd.api+json',
    'X-Auth-Token': 'jtbx8tpu'
}
def getData():
    response = requests.get(url=url, headers=headers)

    routes = list()
    arr = json.loads(response.text)['message']
    for i in arr:
        routes.append(i['points'])
        
    return routes

routes = getData()
print(routes)
conn = psycopg2.connect(database="cabbetmq", user='cabbetmq', password='l910htH7nXV39HJ2xpn0imDE4Dsg0PBs', host='ruby.db.elephantsql.com', port= '5432')
conn.autocommit = True

cursor = conn.cursor()

for f in range(len(routes)):
    for i in range(len(routes[f])):
        cursor.execute(f'''INSERT INTO main_flight(flightid, pointid, sh, distance) VALUES ({f+1}, {i+1}, {routes[f][i]['SH']}, {routes[f][i]['distance']})''')
    
conn.commit()
conn.close()