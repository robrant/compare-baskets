'''
'''
import json

f = open('/Users/robrant/eclipseCode/compare-baskets/geo_app/data/statgeo.json', 'r')
data = json.loads(f.read())
print data

'''
for x in data['arcs']:
    print x

for x in data['objects']['thenewestdict1']['geometries']:
    print x['properties']['Name']

'''