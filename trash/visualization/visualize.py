import folium

def create_map(gdf, file_name='map.html', zoom_start=12):
    m = folium.Map(location=[gdf.centroid.y, gdf.centroid.x], zoom_start=zoom_start)
    folium.GeoJson(gdf).add_to(m)
    m.save(file_name)
    return m