#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import xlrd
import csv

stopTimesXlsx = xlrd.open_workbook('../raw/StopTimesWeekday.xlsx')

print('trip_id,arrival_time,departure_time,stop_id,stop_sequence,stop_headsign,pickup_type,drop_off_type,shape_dist_traveled')
for sheet in stopTimesXlsx.sheets():
    trip_id = sheet.name
    
    stopNums = sheet.col_values(1)[1:]
    poles = sheet.col_values(2)[1:]
    stop_ids = [n + '_' + p for n, p in zip(stopNums, poles)]

    for i in range(3, sheet.ncols):
        arrTimes = sheet.col_values(i)[1:]
        for (arrTime, stop_id, j) in zip(arrTimes, stop_ids, range(0, len(arrTimes))):
            print('w' + trip_id + '-' + str(i - 2) + ',' + arrTime + ',' + arrTime + ',' + stop_id + ',' + str(j)  + ',,,,')

stopTimesXlsx = xlrd.open_workbook('../raw/StopTimesHoliday.xlsx')

for sheet in stopTimesXlsx.sheets():
    trip_id = sheet.name
    
    stopNums = sheet.col_values(1)[1:]
    poles = sheet.col_values(2)[1:]
    stop_ids = [n + '_' + p for n, p in zip(stopNums, poles)]

    for i in range(3, sheet.ncols):
        arrTimes = sheet.col_values(i)[1:]
        for (arrTime, stop_id, j) in zip(arrTimes, stop_ids, range(0, len(arrTimes))):
            print('h' + trip_id + '-' + str(i - 2) + ',' + arrTime + ',' + arrTime + ',' + stop_id + ',' + str(j)  + ',,,,')
