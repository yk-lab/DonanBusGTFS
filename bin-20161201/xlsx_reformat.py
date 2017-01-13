#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import xlrd
import csv
from xlwt import Workbook

routes={}
with open('../gtfs/routes.txt', 'r') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        routes[row[0]] = [row[2],row[3],row[4]]
    sorted(routes)

files = [
            ["../raw/StopTimesWeekday.xlsx", "../raw-20161201/weekday.xlsx", "../ws-20161201/StopTimesWeekday.xlsx", 1],
            ["../raw/StopTimesWeekday.xlsx", "../raw-20161201/holiday.xlsx", "../ws-20161201/StopTimesHoliday.xlsx", 0],
        ]

for file in files:
    print("=== "+file[2]+" ===")
    pStopTimesXlsx = xlrd.open_workbook(file[0])
    error = []
    stopTimesXlsx = xlrd.open_workbook(file[1])
    wb = Workbook()
    for sheet in stopTimesXlsx.sheets():
        if sheet.ncols > 3 and sheet.name.isdigit():
            if sheet.name in pStopTimesXlsx.sheet_names():
                pSheet = pStopTimesXlsx.sheet_by_name(sheet.name)
            else:
                pSheet = None
                error.append(sheet.name)
            ws = wb.add_sheet(sheet.name)
            for i in range(2, sheet.nrows):
                for j in range(3, sheet.ncols):
                    ws.write(i-file[3], j, str(sheet.cell(i, j).value))
            for i in range(2 + file[3], sheet.nrows):
                ws.write(i-file[3], 0, sheet.cell(i, 1).value)
                if pSheet != None and pSheet.nrows == sheet.nrows - 1 - file[3]:
                    if sheet.cell(i, 1).value != pSheet.cell(i-1 - file[3], 0).value:
                        print("Not Match StopName("+sheet.name+"): " + sheet.cell(i, 1).value + "/" + pSheet.cell(i-1 - file[3], 0).value)
                    ws.write(i-file[3], 1, pSheet.cell(i-1 - file[3], 1).value)
                    ws.write(i-file[3], 2, pSheet.cell(i-1 - file[3], 2).value)
                else:
                    error.append(sheet.name)
            if pSheet != None:
                route_id = str(int(pSheet.cell(0, 0).value))
                ws.write( 0, 0, route_id)
                ws.write( 0, 1, routes[route_id][0])
                ws.write( 0, 2, routes[route_id][1])
                ws.write( 0, 3, routes[route_id][2])
            else:
                ws.write( 0, 3, sheet.cell(0,3).value)
                error.append(sheet.name)
    print(sorted(set(error)))
    wb.save(file[2])
