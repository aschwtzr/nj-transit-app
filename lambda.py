import json
import boto3
from collections import defaultdict
s3 = boto3.resource('s3')

# s3_routes_obj = s3.Bucket('nj-transit-app', 'routes.txt')
s3_stops_obj = s3.Object('nj-transit-app', 'stops.txt')
s3_trips_obj = s3.Object('nj-transit-app', 'trips.txt')
s3_stop_times_obj = s3.Object('nj-transit-app', 'stop_times.txt')
routes = {}
stops = {}
trips = {}
stop_times = {}

def load_files():
  # TODO: break out for clarity
  stops_body = s3_stops_obj.get()['Body'].read()

  line_index = 0
  split = stops_body.split(b'\n') 
  for line in split:
    # print(line)
    # print(len(line))
    if len(line) < 3:
      continue
    if line_index > 0:
      decoded = line.decode('utf-8')
      data = decoded.split(',')
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

  trips_body = s3_trips_obj.get()['Body'].read()

  line_index = 0
  split = trips_body.split(b'\n') 
  for line in split:
    if len(line) < 3:
      continue
    if line_index > 0:
      decoded = line.decode(encoding="UTF-8")
      data = decoded.split(',')
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
  # print(trips)

  stop_times_body = s3_stop_times_obj.get()['Body'].read()

  line_index = 0
  split = stop_times_body.split(b'\n') 
  for line in split:
    if len(line) < 2:
      continue
    if line_index > 0:
      decoded = line.decode(encoding="UTF-8")
      data = decoded.split(',')

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
  filtered = {}
  destination_trips = defaultdict(list)
  for id, stop in stop_times.items():
    if stop['stop_id'] == destination:
      destination_trips[stop['trip_id']].append(id)
  for id, stop in stop_times.items():
    if (stop['stop_id'] == origin):
      if destination_trips[stop['trip_id']]:
        filtered[id] = stop
  return filtered
  
def lambda_handler(event, context):
  load_files()

  destination = event['destination']
  origin = event['origin']

  results = find_stops(destination, origin)

  return {
      'statusCode': 200,
      'body': json.dumps([results])
  }
  