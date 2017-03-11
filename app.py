import json
import requests
import googlemaps
from datetime import datetime

api = 'AIzaSyDndb2zL0PSf0e8JqesZHJIsoqOnhLJf0M'

origin = '268 Philips Street, Waterloo'
dest = '7 Brighton Place Unit 18, Thornhill'

gmaps = googlemaps.Client(key=api)

directions = gmaps.directions(
        origin = origin,
        destination = dest,
        waypoints = ['7223 Dishley Court, Mississauga',
            'Finch Station, Toronto'],
        mode='driving')

print directions

with open('directions2.txt', 'w') as outfile:
    json.dump(directions, outfile)
