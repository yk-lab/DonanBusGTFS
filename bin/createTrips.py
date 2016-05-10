#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import xlrd

print('route_id,service_id,trip_id,trip_headsign,trip_short_name,direction_id,block_id,shape_id')

stopTimesXlsx = xlrd.open_workbook('../raw/StopTimesWeekday.xlsx')
for sheet in stopTimesXlsx.sheets():
    route_id = str(int(sheet.cell(0, 0).value))
    trip_id = sheet.name
    for i in range(sheet.ncols - 3):
        print(route_id + ',dn_weekday,w' + trip_id + '-' + str(i + 1) + ',,,,,')

stopTimesXlsxHoliday = xlrd.open_workbook('../raw/StopTimesHoliday.xlsx')
for sheet in stopTimesXlsxHoliday.sheets():
    route_id = str(int(sheet.cell(0, 0).value))
    trip_id = sheet.name
    for i in range(sheet.ncols - 3):
        print(route_id + ',dn_holiday,h' + trip_id + '-' + str(i + 1) + ',,,,,')
