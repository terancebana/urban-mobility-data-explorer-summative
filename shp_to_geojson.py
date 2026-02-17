import geopandas as gpd
import os

shp_path = "data/taxi_zones/taxi_zones.shp"
output_path = "web/assets/taxi_zones.json"

print(f"Reading shapefile from {shp_path}...")
try:
    gdf = gpd.read_file(shp_path)

    print(f"Original CRS: {gdf.crs}")

    if gdf.crs.to_string() != "EPSG:4326":
        print("Reprojecting to EPSG:4326...")
        gdf = gdf.to_crs(epsg=4326)

    print(f"Saving GeoJSON to {output_path}...")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    gdf.to_file(output_path, driver="GeoJSON")
    print("Conversion successful!")

except Exception as e:
    print(f"Error converting shapefile: {e}")
