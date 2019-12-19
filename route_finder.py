import json
from collections import defaultdict

routes = {}
stops = {}
trips = {}
stop_times = {}

def load_transit_data ():
  with open("./rail_data/routes.txt") as file:
    line_index = 0
    for line in file:
      if line_index > 0:
        data = line.split(',')
        routes[line_index] = {
          'route_id': int(data[0]),
          'agency_id': data[1].replace('"', ''),
          'route_short_name': data[2].replace('"', ''),
          'route_long_name': data[3].replace('"', ''),
          'route_type': int(data[4]),
          'route_url': data[5].replace('"', ''),
          'route_colour': data[6].replace('\n', '')
        } 
      line_index += 1

  with open('./rail_data/stops.txt') as file:
    line_index = 0
    for line in file:
      if line_index > 0:
        data = line.split(',')
        stops[line_index] = {
          'stop_id': int(data[0]),
          'stop_code': int(data[1]),
          'stop_name': data[2].replace('"', ''),
          'stop_desc': data[3].replace('"', ''),
          'stop_lat': float(data[4]),
          'stop_lon': float(data[5]),
          'zone_id': data[6].replace('\n', '')
        } 
      line_index += 1

  with open("./rail_data//trips.txt") as file:
    line_index = 0
    for line in file:
      if line_index > 0:
        data = line.split(',')
        trips[line_index] = {
          'route_id': int(data[0]),
          'service_id': int(data[1]),
          'trip_id': int(data[2]),
          'trip_headsign': data[3].replace('"', ''),
          'direction_id': int(data[4]),
          'block_id': data[5].replace('"', ''),
          'shape_id': int(data[6])
        } 
      line_index += 1

  with open("./rail_data/stop_times.txt") as file:
    line_index = 0
    for line in file:
      if line_index > 0:
        data = line.split(',')
        stop_times[line_index] = {
          'trip_id': int(data[0]),
          'arrival_time': data[1],
          'departure_time': data[2],
          'stop_id': int(data[3]),
          'stop_sequence': int(data[4]),
          'pickup_type': int(data[5]),
          'drop_off_type': int(data[6]),
          'shape_dist_traveled': float(data[7])
        } 
      line_index += 1

def find_stops (origin, destination):
  load_transit_data()
  filtered = {}
  destination_trips = defaultdict(list)

  for id, stop in stop_times.items():
    if stop['stop_id'] == int(destination):
      print(stop['stop_id'] == int(destination))
      destination_trips[stop['trip_id']].append(id)
  print(destination_trips)
  for id, stop in stop_times.items():
    if (stop['stop_id'] == int(origin)):
      if destination_trips[stop['trip_id']]:
        filtered[id] = stop
  print(filtered)
  return filtered

def get_stations ():
  load_transit_data()
  return stops