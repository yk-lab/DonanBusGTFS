#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import xlrd
import csv

routes = {}

agency_id = "donanbus"
files = ['../ws-20161201/StopTimesWeekday.xlsx', '../ws-20161201/StopTimesHoliday.xlsx']
for file in files:
    stopTimesXlsx = xlrd.open_workbook(file)
    for sheet in stopTimesXlsx.sheets():
        if sheet.ncols > 0 and sheet.cell(0, 0).value != None and sheet.cell(0, 0).value != "":
            route_id = str(int(sheet.cell(0, 0).value))
            if route_id not in routes:
                routes[route_id] = [str(sheet.cell(0, 1).value),str(sheet.cell(0, 2).value),str(sheet.cell(0, 3).value)]


print('route_id,agency_id,route_short_name,route_long_name,route_desc,route_type,route_url,route_color,route_text_color')
for key in sorted(routes.keys()):
    route_id = key
    route_short_name = routes[key][0]
    route_long_name = routes[key][1]
    route_desc = routes[key][2]
    route_type = "3"
    route_url = ""
    route_color = ""
    route_text_color = ""
    print("%s,%s,%s,%s,%s,%s,%s,%s,%s" % (route_id, agency_id,route_short_name,route_long_name,route_desc,route_type,route_url,route_color,route_text_color))
