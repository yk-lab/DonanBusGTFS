#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import xlrd
import csv

def findName(csvlist, sid):
  if (csvlist[0]['stop_id'] == sid):
    return csvlist[0]['stop_id']
  else:
    return findName(csvlist[1:], sid)

stopTimesXlsx = xlrd.open_workbook('../raw/StopTimesWeekday.xlsx')
stopsCsvFile = list(csv.DictReader(open('../gtfs/stops.txt', 'r')))

for sheet in stopTimesXlsx.sheets():
    stopNums = sheet.col_values(1)[1:]
    poles = sheet.col_values(2)[1:]
    stop_ids = [n + '_' + p for n, p in zip(stopNums, poles)]
    for ids in stop_ids:
      if ids != findName(stopsCsvFile, ids):
        print(ids)


#stopTimesXlsx = xlrd.open_workbook('../raw/StopTimesHoliday.xlsx')
#
#for sheet in stopTimesXlsx.sheets():
#    trip_id = sheet.name
#    
#    stopNums = sheet.col_values(1)[1:]
#    poles = sheet.col_values(2)[1:]
#    stop_ids = [n + '_' + p for n, p in zip(stopNums, poles)]
#
#    for i in range(3, sheet.ncols):
#        arrTimes = sheet.col_values(i)[1:]
#        for (arrTime, stop_id, j) in zip(arrTimes, stop_ids, range(0, len(arrTimes))):
#            print('h' + trip_id + '-' + str(i - 2) + ',' + arrTime + ',' + arrTime + ',' + stop_id + ',' + str(j)  + ',,,,')
