#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import csv

# MariaDBへの接続
conn = sqlite3.connect("donanbus.db")

dbCursor = conn.cursor()

# テーブルの作成
dbCursor.execute("""CREATE TABLE IF NOT EXISTS agency(
agency_id       TEXT NULL,
agency_name     TEXT NOT NULL,
agency_url      TEXT NOT NULL,
agency_timezone TEXT NOT NULL,
agency_lang     TEXT NULL,
agency_phone    TEXT NULL,
agency_fare_url TEXT NULL);
""".strip())

dbCursor.execute("""CREATE TABLE IF NOT EXISTS stops(
stop_id             TEXT NOT NULL,
stop_code           TEXT NULL,
stop_name           TEXT NOT NULL,
stop_desc           TEXT NULL,
stop_lat            REAL NOT NULL,
stop_lon            REAL NOT NULL,
zone_id             TEXT NULL,
stop_url            TEXT NULL,
location_type       INTEGER NULL DEFAULT 0,
parent_station      INTEGER NULL,
stop_timezone       TEXT NULL,
wheelchair_boarding INTEGER NULL DEFAULT 0);
""".strip())

dbCursor.execute("""CREATE TABLE IF NOT EXISTS routes(
route_id         TEXT NOT NULL,
agency_id        TEXT NULL,
route_short_name TEXT NOT NULL,
route_long_name  TEXT NOT NULL,
route_desc       TEXT NULL,
route_type       INTEGER NOT NULL DEFAULT 3,
route_url        TEXT NULL,
route_color      TEXT NULL,
route_text_color TEXT NULL);
""".strip())

dbCursor.execute("""CREATE TABLE IF NOT EXISTS trips(
route_id        TEXT NOT NULL,
service_id      TEXT NOT NULL,
trip_id         TEXT NOT NULL,
trip_headsign   TEXT NULL,
trip_short_name TEXT NULL,
direction_id    INTEGER NULL,
block_id        TEXT NULL,
shape_id        TEXT NULL);
""".strip())

dbCursor.execute("""CREATE TABLE IF NOT EXISTS stoptimes(
trip_id             TEXT NOT NULL,
arrival_time        TEXT NOT NULL,
departure_time      TEXT NOT NULL,
stop_id             TEXT NOT NULL,
stop_sequence       INTEGER NOT NULL,
stop_headsign       TEXT NULL,
pickup_type         INTEGER NULL DEFAULT 0,
drop_off_type       INTEGER NULL DEFAULT 0,
shape_dist_traveled TEXT NULL);
""".strip())

dbCursor.execute("""CREATE TABLE IF NOT EXISTS calendar(
service_id TEXT NOT NULL,
monday     INTEGER NOT NULL,
tuesday    INTEGER NOT NULL,
wednesday  INTEGER NOT NULL,
thursday   INTEGER NOT NULL,
friday     INTEGER NOT NULL,
saturday   INTEGER NOT NULL,
sunday     INTEGER NOT NULL,
start_date TEXT NOT NULL,
end_date   TEXT NOT NULL);
""".strip())

conn.commit()

# DBへの登録
agencyCsv = csv.reader(open('../gtfs/agency.txt', 'r'))
agencyHeader = next(agencyCsv)
for row in agencyCsv:
  dbCursor.execute('INSERT INTO agency VALUES(?, ?, ?, ?, ?, ?, ?)', tuple(row))

stopsCsv = csv.reader(open('../gtfs/stops.txt', 'r'))
stopsHeader = next(stopsCsv)
for row in stopsCsv:
  dbCursor.execute('INSERT INTO stops VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', tuple(row))

routesCsv = csv.reader(open('../gtfs/routes.txt', 'r'))
routesHeader = next(routesCsv)
for row in routesCsv:
  dbCursor.execute('INSERT INTO routes VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)', tuple(row))

tripsCsv = csv.reader(open('../gtfs/trips.txt', 'r'))
tripsHeader = next(tripsCsv)
for row in tripsCsv:
  dbCursor.execute('INSERT INTO trips VALUES(?, ?, ?, ?, ?, ?, ?, ?)', tuple(row))

stopTimesCsv = csv.reader(open('../gtfs/stop_times.txt', 'r'))
stopTimesHeader = next(stopTimesCsv)
for row in stopTimesCsv:
  dbCursor.execute('INSERT INTO stop_times VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)', tuple(row))

calendarCsv = csv.reader(open('../gtfs/calendar.txt', 'r'))
calendarHeader = next(calendarCsv)
for row in calendarCsv:
  dbCursor.execute('INSERT INTO calendar VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', tuple(row))

# DB切断
conn.commit()
dbCursor.close()
conn.close()
