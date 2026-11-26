import json

with open(
    "data/geojson/fj.json",
    "r",
    encoding="utf-8"
) as f:
    geojson = json.load(f)

print("\nDIVISIONS FOUND IN GEOJSON\n")

for feature in geojson["features"]:
    print(feature["properties"]["name"])