#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import psycopg2
import csv

# MariaDBへの接続
client = psycopg2.connect("host=localhost dbname=donanbus user=postgres password=" + os.environ['PASS'])

dbCursor = client.cursor()

# テーブルの作成
dbCursor.execute("""
CREATE TABLE IF NOT EXISTS Agency(
agency_id       VARCHAR UNIQUE NULL,
agency_name     VARCHAR NOT NULL,
agency_url      VARCHAR NOT NULL,
agency_timezone VARCHAR NOT NULL,
agency_lang     VARCHAR NULL,
agency_phone    VARCHAR NULL,
agency_fare_url VARCHAR NULL
)
""".strip())
client.commit()

dbCursor.execute("""
CREATE TABLE IF NOT EXISTS Calendar(
service_id VARCHAR NOT NULL UNIQUE PRIMARY KEY,
monday     INT     NOT NULL,
tuesday    INT     NOT NULL,
wednesday  INT     NOT NULL,
thursday   INT     NOT NULL,
friday     INT     NOT NULL,
saturday   INT     NOT NULL,
sunday     INT     NOT NULL,
start_date VARCHAR NOT NULL,
end_date   VARCHAR NOT NULL
)
""".strip())
client.commit()

dbCursor.execute("""
CREATE TABLE IF NOT EXISTS Stops(
stop_id             VARCHAR NOT NULL UNIQUE PRIMARY KEY,
stop_code           VARCHAR NULL,
stop_name           VARCHAR NOT NULL,
stop_desc           VARCHAR NULL,
stop_lat            DOUBLE PRECISION NOT NULL,
stop_lon            DOUBLE PRECISION NOT NULL,
zone_id             VARCHAR NULL,
stop_url            VARCHAR NULL,
location_type       INT     NULL DEFAULT 0,
parent_station      INT     NULL,
stop_timezone       VARCHAR NULL,
wheelchair_boarding INT     NULL DEFAULT 0
)
""".strip())

dbCursor.execute("""
CREATE TABLE IF NOT EXISTS Routes(
route_id         VARCHAR NOT NULL UNIQUE PRIMARY KEY,
agency_id        VARCHAR NULL REFERENCES Agency(agency_id),
route_short_name VARCHAR NOT NULL,
route_long_name  VARCHAR NOT NULL,
route_desc       VARCHAR NULL,
route_type       INT     NOT NULL,
route_url        VARCHAR NULL,
route_color      VARCHAR NULL,
route_text_color VARCHAR NULL
)
""".strip())

dbCursor.execute("""
CREATE TABLE IF NOT EXISTS Trips(
route_id        VARCHAR NOT NULL REFERENCES Routes(route_id),
service_id      VARCHAR NOT NULL REFERENCES Calendar(service_id),
trip_id         VARCHAR NOT NULL UNIQUE PRIMARY KEY,
trip_headsign   VARCHAR NULL,
trip_short_name VARCHAR NULL,
direction_id    INT     NULL,
block_id        VARCHAR NULL,
shape_id        VARCHAR NULL
)
""".strip())

dbCursor.execute("""
CREATE TABLE IF NOT EXISTS StopTimes(
trip_id             VARCHAR NOT NULL REFERENCES Trips(trip_id),
arrival_time        VARCHAR NOT NULL,
departure_time      VARCHAR NOT NULL,
stop_id             VARCHAR NOT NULL REFERENCES Stops(stop_id),
stop_sequence       INT     NOT NULL,
stop_headsign       VARCHAR NULL,
pickup_type         INT     NULL DEFAULT 0,
drop_off_type       INT     NULL DEFAULT 0,
shape_dist_traveled VARCHAR NULL
)
""".strip())

client.commit()

# Indexの作成
dbCursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS agency_index   ON Agency   (agency_id)")
dbCursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS calendar_index ON Calendar (service_id)")
dbCursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS stops_index    ON Stops    (stop_id)")
dbCursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS routes_index   ON Routes   (route_id)")
dbCursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS trips_index    ON Trips    (trip_id)")

client.commit()

# DBへの登録
agencyCsv = csv.reader(open('../gtfs/agency.txt', 'r'))
agencyHeader = next(agencyCsv)
for row in agencyCsv:
  dbCursor.execute('INSERT INTO Agency VALUES (%s, %s, %s, %s, %s, %s, %s)', tuple(row))

calendarCsv = csv.reader(open('../gtfs/calendar.txt', 'r'))
calendarHeader = next(calendarCsv)
for row in calendarCsv:
  dbCursor.execute('INSERT INTO Calendar values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', \
    (row[0], int(row[1]), int(row[2]), int(row[3]), int(row[4]), int(row[5]), int(row[6]), int(row[7]), row[8], row[9]))

stopsCsv = csv.reader(open('../gtfs/stops.txt', 'r'))
stopsHeader = next(stopsCsv)
for row in stopsCsv:
  dbCursor.execute('INSERT INTO Stops (stop_id, stop_name, stop_lat, stop_lon) values(%s, %s, %s, %s)', \
    (row[0], row[2], float(row[4]), float(row[5])))

routesCsv = csv.reader(open('../gtfs/routes.txt', 'r'))
routesHeader = next(routesCsv)
for row in routesCsv:
  dbCursor.execute('INSERT INTO Routes (route_id, agency_id, route_short_name, route_long_name, route_desc, route_type) values(%s, %s, %s, %s, %s, %s)', \
    (row[0], row[1], row[2], row[3], row[4], row[5]))

tripsCsv = csv.reader(open('../gtfs/trips.txt', 'r'))
tripsHeader = next(tripsCsv)
for row in tripsCsv:
  dbCursor.execute('INSERT INTO Trips (route_id,service_id,trip_id) values(%s, %s, %s)', \
    (row[0], row[1], row[2]))

stopTimesCsv = csv.reader(open('../gtfs/stop_times.txt', 'r'))
stopTimesHeader = next(stopTimesCsv)
for row in stopTimesCsv:
  dbCursor.execute('INSERT INTO StopTimes (trip_id, arrival_time, departure_time, stop_id, stop_sequence) values(%s, %s, %s, %s, %s)', \
    (row[0], row[1] + ':00', row[2] + ':00', row[3], int(row[4])))

client.commit()

# DB切断
dbCursor.close()
client.close()
