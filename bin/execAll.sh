#!/usr/bin/env sh
./createStops.py > ../gtfs/stops.txt
./createTrips.py > ../gtfs/trips.txt
./createStopTimes.py > ../gtfs/stop_times.txt