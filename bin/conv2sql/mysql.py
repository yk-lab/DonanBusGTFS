#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pymysql
import csv
import os

# MariaDBへの接続
client = pymysql.connect(
  host = 'localhost',
  user = 'root',
  password = os.environ['PASS'],
  db = 'donanbus',
  charset = 'utf8',
  cursorclass=pymysql.cursors.DictCursor
)

dbCursor = client.cursor()

# テーブルの作成
dbCursor.execute("""
CREATE TABLE IF NOT EXISTS Agency(
agency_id       CHAR(16)   NULL,
agency_name     CHAR(64)   NOT NULL,
agency_url      CHAR(128)  NOT NULL,
agency_timezone CHAR(16)   NOT NULL,
agency_lang     CHAR(4)    NULL,
agency_phone    CHAR(16)   NULL,
agency_fare_url CHAR(128)  NULL,
INDEX(agency_id)
) ENGINE = innoDB
""".strip())
client.commit()

dbCursor.execute("""
CREATE TABLE IF NOT EXISTS Calendar(
service_id CHAR(16) NOT NULL PRIMARY KEY,
monday     INT      NOT NULL,
tuesday    INT      NOT NULL,
wednesday  INT      NOT NULL,
thursday   INT      NOT NULL,
friday     INT      NOT NULL,
saturday   INT      NOT NULL,
sunday     INT      NOT NULL,
start_date CHAR(16) NOT NULL,
end_date   CHAR(16) NOT NULL,
INDEX(service_id)
) ENGINE = innoDB
""".strip())
client.commit()

dbCursor.execute("""
CREATE TABLE IF NOT EXISTS Stops(
stop_id             CHAR(8)   NOT NULL PRIMARY KEY,
stop_code           CHAR(32)  NULL,
stop_name           CHAR(64)  NOT NULL,
stop_desc           CHAR(128) NULL,
stop_lat            DOUBLE    NOT NULL,
stop_lon            DOUBLE    NOT NULL,
zone_id             CHAR(8)   NULL,
stop_url            CHAR(128) NULL,
location_type       INT       NULL DEFAULT 0,
parent_station      INT       NULL,
stop_timezone       CHAR(16)  NULL,
wheelchair_boarding INT       NULL DEFAULT 0,
INDEX(stop_id)
) ENGINE = innoDB
""".strip())
client.commit()

dbCursor.execute("""
CREATE TABLE IF NOT EXISTS Routes(
route_id         CHAR(16)  NOT NULL PRIMARY KEY,
agency_id        CHAR(16)  NULL,
route_short_name CHAR(128) NOT NULL,
route_long_name  CHAR(128) NOT NULL,
route_desc       CHAR(128) NULL,
route_type       INT       NOT NULL,
route_url        CHAR(128) NULL,
route_color      CHAR(8)   NULL,
route_text_color CHAR(8)   NULL,
INDEX(route_id),
FOREIGN KEY (agency_id) REFERENCES Agency(agency_id)
) ENGINE = innoDB
""".strip())
client.commit()

dbCursor.execute("""
CREATE TABLE IF NOT EXISTS Trips(
route_id        CHAR(16)  NOT NULL,
service_id      CHAR(16)  NOT NULL,
trip_id         CHAR(16)  NOT NULL PRIMARY KEY,
trip_headsign   CHAR(64)  NULL,
trip_short_name CHAR(128) NULL,
direction_id    INT       NULL,
block_id        CHAR(16)  NULL,
shape_id        CHAR(16)  NULL,
INDEX(trip_id),
FOREIGN KEY (route_id) REFERENCES Routes(route_id),
FOREIGN KEY (service_id) REFERENCES Calendar(service_id)
) ENGINE = innoDB
""".strip())
client.commit()

dbCursor.execute("""
CREATE TABLE IF NOT EXISTS StopTimes(
trip_id             CHAR(16)  NOT NULL,
arrival_time        CHAR(16)  NOT NULL,
departure_time      CHAR(16)  NOT NULL,
stop_id             CHAR(8)   NOT NULL,
stop_sequence       INT       NOT NULL,
stop_headsign       CHAR(128) NULL,
pickup_type         INT       NULL DEFAULT 0,
drop_off_type       INT       NULL DEFAULT 0,
shape_dist_traveled CHAR(16)  NULL,
FOREIGN KEY (trip_id) REFERENCES Trips(trip_id),
FOREIGN KEY (stop_id) REFERENCES Stops(stop_id)
) ENGINE = innoDB
""".strip())
client.commit()

# DBへの登録
agencyCsv = csv.reader(open('../gtfs/agency.txt', 'r'))
agencyHeader = next(agencyCsv)
for row in agencyCsv:
  dbCursor.execute('INSERT INTO Agency values(%s, %s, %s, %s, %s, %s, %s)', tuple(row))

calendarCsv = csv.reader(open('../gtfs/calendar.txt', 'r'))
calendarHeader = next(calendarCsv)
for row in calendarCsv:
  dbCursor.execute('INSERT INTO Calendar values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', tuple(row))

stopsCsv = csv.reader(open('../gtfs/stops.txt', 'r'))
stopsHeader = next(stopsCsv)
for row in stopsCsv:
  dbCursor.execute('INSERT INTO Stops values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', tuple(row))

routesCsv = csv.reader(open('../gtfs/routes.txt', 'r'))
routesHeader = next(routesCsv)
for row in routesCsv:
  dbCursor.execute('INSERT INTO Routes values(%s, %s, %s, %s, %s, %s, %s, %s, %s)', tuple(row))

tripsCsv = csv.reader(open('../gtfs/trips.txt', 'r'))
tripsHeader = next(tripsCsv)
for row in tripsCsv:
  dbCursor.execute('INSERT INTO Trips values(%s, %s, %s, %s, %s, %s, %s, %s)', tuple(row))

stopTimesCsv = csv.reader(open('../gtfs/stop_times.txt', 'r'))
stopTimesHeader = next(stopTimesCsv)
for row in stopTimesCsv:
  dbCursor.execute('INSERT INTO StopTimes values(%s, %s, %s, %s, %s, %s, %s, %s, %s)', (row[0], row[1] + ':00', row[2] + ':00', row[3], row[4], row[5], row[6], row[7], row[8]))

client.commit()

# DB切断
dbCursor.close()
client.close()
