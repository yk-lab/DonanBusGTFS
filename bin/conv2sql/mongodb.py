#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pymongo
import csv

def insertCsvData(fileName, collection):
  csvFile = csv.DictReader(open('../gtfs/' + fileName, 'r'))
  for row in csvFile:
    collection.insert_one(row)

# MongoDBへの接続
client = pymongo.MongoClient('localhost', 27017)

# DBの作成
donanbusDb = client.donanbus

# agency.txtをDBに書き込む
insertCsvData('agency.txt', donanbusDb.agency)

insertCsvData('calendar.txt', donanbusDb.calendar)

insertCsvData('routes.txt', donanbusDb.routes)

insertCsvData('stop_times.txt', donanbusDb.stop_times)

insertCsvData('stops.txt', donanbusDb.stops)

insertCsvData('trips.txt', donanbusDb.trips)
