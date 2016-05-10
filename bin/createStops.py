#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, urllib.request, urllib.error

# OSMのAPIからJSONを取り出す
def fetchOsmJson():
    try:
        url = 'http://overpass-api.de/api/interpreter?data=%5Bout%3Ajson%5D%3Barea%5B%22name%22%7E%22%E5%AE%A4%E8%98%AD%E5%B8%82%7C%E7%99%BB%E5%88%A5%E5%B8%82%22%5D%3Bnode%28area%29%5B%22highway%22%3D%22bus%5Fstop%22%5D%3Bout%20body%3B%0A'
        req = urllib.request.urlopen(url)
        loadedJson = json.loads(req.read().decode('utf-8'))
        return loadedJson['elements']
    except:
        req.close()
        return ['Failed']

# OSMのAPIからJSONを取り出す
busStops = fetchOsmJson()

# refが定義されてない要素を外す
errorDeleted = filter(lambda stop: "ref" in stop['tags'], busStops)
# id, name, lat, lonを抽出
formatFixed = map(lambda stop: {'id':stop['tags']['ref'],'name':stop['tags']['name'],'lat':stop['lat'],'lon':stop['lon']}, errorDeleted)

# ソートしてからCSVとして出力
print("stop_id,stop_code,stop_name,stop_desc,stop_lat,stop_lon,zone_id,stop_url,location_type,parent_station,stop_timezone,wheelchair_boarding")
for stop in sorted(formatFixed, key = lambda s: s['id']):
    # idが複数ある場合は分けて出力
    for sid in stop['id'].split():
        print(sid + ",," + stop['name'] + ",," + str(stop['lat']) + ',' + str(stop['lon']) + ",,,,,,")
