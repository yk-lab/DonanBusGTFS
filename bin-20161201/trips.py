#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import xlrd
import re

print('route_id,service_id,trip_id,trip_headsign,trip_short_name,direction_id,block_id,shape_id')
files = ['../ws-20161201/StopTimesWeekday.xlsx', '../ws-20161201/StopTimesHoliday.xlsx']
services = ["dn_20161201_weekday", "dn_20161201_holiday", "dn_20161201_schoolday"]

for k, file in enumerate(files):
    stopTimesXlsx = xlrd.open_workbook(file)
    for sheet in stopTimesXlsx.sheets():
        if sheet.ncols > 0 and sheet.cell(0, 0).value != None and str(sheet.cell(0, 0).value) != "":
            route_id = str(sheet.cell(0, 0).value)
            trip_id = str(sheet.name)
            trip_headsign = ""
            trip_short_name = ""
            direction_id = ""
            block_id = ""
            shape_id = ""
            if sheet.ncols > 0:
                for i in range(sheet.ncols - 3):
                    if re.match(r"\w*●\w*", str(sheet.cell(1, i + 3).value)):
                        service_id = "dn_20161201_schoolday"
                        prefix = "s"
                    else:
                        service_id = services[k]
                        prefix = "w" if k == 0 else "h"
                    print("%s,%s,%s,%s,%s,%s,%s,%s" % (route_id, service_id, prefix + trip_id + '-' + str(i + 1), trip_headsign, trip_short_name, direction_id, block_id, shape_id) )
