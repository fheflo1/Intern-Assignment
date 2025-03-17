import json

with open('./data/AnadromeLaksefisk_0000_norge_4326_GEOJSON.geojson') as f:
    data = json.load(f)

geojson_data = data['AnadromBestand']

with open('./data/AnadromeLaksefisk_fixed.geojson', 'w') as f:
    json.dump(geojson_data, f)

print("✅ GeoJSON-filen er fikset!")
