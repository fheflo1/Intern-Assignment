import json

# Åpne og les originalfilen din
with open('./data/AnadromeLaksefisk_0000_norge_4326_GEOJSON.geojson') as f:
    data = json.load(f)

# Hent ut den korrekte delen ("FeatureCollection")
geojson_data = data['AnadromBestand']

# Lagre det på riktig format igjen
with open('./data/AnadromeLaksefisk_fixed.geojson', 'w') as f:
    json.dump(geojson_data, f)

print("✅ GeoJSON-filen er fikset!")
