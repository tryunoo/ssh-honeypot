#!/usr/bin/python3
# -*- coding: utf-8 -*-
from elasticsearch import Elasticsearch
from datetime import datetime
import geoip2.database
import time
import json

es = Elasticsearch("localhost:9200")

dic = {}

#dic["date"] = '2018-11-16 17:37:11'
dic["date"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#dic["date"] = datetime.now().timestamp()
dic["clientip"] = '217.168.76.77'
dic["username"] = 'root'
dic["password"] = 'password'
#dic["clientip"] = '192.168.1.5'

try:
	reader = geoip2.database.Reader('./GeoLite2-City.mmdb')
	res = reader.city(dic['clientip'])

	#dic["country"] = res.country.names["en"]
	dic["geo_point"] = {"lat":res.location.latitude, "lon": res.location.longitude}
	dic["country"] = res.country.iso_code
except:
	pass

json_data = json.dumps(dic)

res = es.index(index="ssh", doc_type="_doc", body=json_data)

print(dic['date'])
print(res)