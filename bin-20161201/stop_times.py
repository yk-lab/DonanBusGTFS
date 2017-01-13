#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import xlrd
import re

files = ['../ws-20161201/StopTimesWeekday.xlsx', '../ws-20161201/StopTimesHoliday.xlsx']
services = ["dn_20161201_weekday", "dn_20161201_holiday", "dn_20161201_schoolday"]

print("trip_id,arrival_time,departure_time,stop_id,stop_sequence,stop_headsign,pickup_type,drop_off_type,shape_dist_traveled")
for k, file in enumerate(files):
    stopTimesXlsx = xlrd.open_workbook(file)
    for sheet in stopTimesXlsx.sheets():
        trip_id = sheet.name

        stopNums = sheet.col_values(1)[2:]
        poles = sheet.col_values(2)[2:]
        stop_ids = [n + '_' + p for n, p in zip(stopNums, poles)]

        if sheet.ncols > 3 and sheet.cell(0,0).value != "":
            for i in range(3, sheet.ncols):
                if re.match(r"\w*●\w*", str(sheet.cell(1, i).value)):
                    service_id = "dn_20161201_schoolday"
                    prefix = "s"
                else:
                    service_id = services[k]
                    prefix = "w" if k == 0 else "h"
                arrTimes = sheet.col_values(i)[2:]
                for (arrTime, stop_id, j) in zip(arrTimes, stop_ids, range(0, len(arrTimes))):
                    print(prefix + trip_id + '-' + str(i - 2) + ',' + arrTime + ',' + arrTime + ',' + stop_id + ',' + str(j)  + ',,,,')
