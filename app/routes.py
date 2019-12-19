from app import app
import route_finder
import json
from flask import request

@app.route('/')
def index():
    return json.dumps({ 'ok': True })

@app.route('/routes')
def get_routes():
  origin = request.args.get('origin')
  destination = request.args.get('destination')
  # results = route_finder.find_stops(40570, 38174)
  results = route_finder.find_stops(origin, destination)
  # print(results)
  return json.dumps([results])

@app.route('/stations')
def get_stations():
  results = route_finder.get_stations()
  return json.dumps([results])