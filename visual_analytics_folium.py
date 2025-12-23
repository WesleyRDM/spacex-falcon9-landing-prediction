# -*- coding: utf-8 -*-
"""Visual_Analytics_Folium.ipynb

import folium
import pandas as pd
from folium.plugins import MarkerCluster
from folium.plugins import MousePosition
from folium.features import DivIcon

world_map = folium.Map()
world_map

import requests
import io

URL = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_geo.csv'
resp = requests.get(URL)
spacex_csv_file = io.BytesIO(resp.content)
spacex_df=pd.read_csv(spacex_csv_file)

spacex_df = spacex_df[['Launch Site', 'Lat', 'Long', 'class']]
launch_sites_df = spacex_df.groupby(['Launch Site'], as_index=False).first()
launch_sites_df = launch_sites_df[['Launch Site', 'Lat', 'Long']]
launch_sites_df

nasa_coordinate = [29.559684888503615, -95.0830971930759]
site_map = folium.Map(location=nasa_coordinate, zoom_start=10)

circle = folium.Circle(nasa_coordinate, radius=1000, color='#d35400', fill=True).add_child(folium.Popup('NASA Johnson Space Center'))
marker = folium.map.Marker(
                  nasa_coordinate,
                  icon=DivIcon(
                      icon_size=(20,20),
                      icon_anchor=(0,0),
                      html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % 'NASA JSC',
                      )
    )
site_map.add_child(circle)
site_map.add_child(marker)

site_map = folium.Map(location=nasa_coordinate, zoom_start=5)

for index, row in launch_sites_df.iterrows():
    launch_site_name = row['Launch Site']
    site_lat = row['Lat']
    site_long = row['Long']
    site_coordinate = [site_lat, site_long]

    circle = folium.Circle(site_coordinate, radius=1000, color='#000000', fill=True).add_child(folium.Popup(launch_site_name))
    site_map.add_child(circle)

    marker = folium.map.Marker(
        site_coordinate,
        icon=DivIcon(
            icon_size=(20,20),
            icon_anchor=(0,0),
            html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % launch_site_name,
        )
    )
    site_map.add_child(marker)

site_map

marker_map = folium.Map(location=nasa_coordinate, zoom_start=5)

marker_cluster = MarkerCluster()

def assign_marker_color(launch_outcome):
    if launch_outcome == 1:
        return 'green'
    else:
        return 'red'

marker_map.add_child(marker_cluster)
for index, row in spacex_df.iterrows():
    launch_site = row['Launch Site']
    coordinate = [row['Lat'], row['Long']]
    class_outcome = row['class']

    marker_color = assign_marker_color(class_outcome)
    marker = folium.CircleMarker(
        location=coordinate,
        radius=5,
        color=marker_color,
        fill=True,
        fill_color=marker_color,
        fill_opacity=0.7,
        popup=f"Launch Site: {launch_site}\nOutcome: {'Success' if class_outcome == 1 else 'Failure'}"
    )
    marker_cluster.add_child(marker)

marker_map

spacex_df.tail(10)

site_map.add_child(marker_cluster)
for index, record in spacex_df.iterrows():
    marker_cluster.add_child(marker)

site_map

"""### Task 3: Calculate the distances between a launch site to its proximities"""

from math import sin, cos, sqrt, atan2, radians

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6373.0

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance

"""Next, we need to find the coordinates of a few interesting points around the launch sites, such as:
*   A nearby city (e.g., Cocoa Beach)
*   A nearby road (e.g., Florida State Road 3)
*   A nearby coastline point
"""

launch_site_lat = launch_sites_df.loc[0, 'Lat']
launch_site_lon = launch_sites_df.loc[0, 'Long']

# Example of a nearest city (Cocoa Beach, Florida)
city_lat, city_lon = 28.3249, -80.6077
distance_city = calculate_distance(launch_site_lat, launch_site_lon, city_lat, city_lon)

# Example of a nearest railway (Approximation near Cape Canaveral)
railway_lat, railway_lon = 28.5721, -80.5852
distance_railway = calculate_distance(launch_site_lat, launch_site_lon, railway_lat, railway_lon)

# Example of a nearest highway (Approximation of FL-3)
highway_lat, highway_lon = 28.5638, -80.5708
distance_highway = calculate_distance(launch_site_lat, launch_site_lon, highway_lat, highway_lon)

# The provided coordinates for a nearest coastline point
coastline_lat, coastline_lon = 28.56367, -80.57163
distance_coastline = calculate_distance(launch_site_lat, launch_site_lon, coastline_lat, coastline_lon)

print(f"Distance from CCAFS LC-40 to nearest city: {distance_city:.2f} km")
print(f"Distance from CCAFS LC-40 to nearest railway: {distance_railway:.2f} km")
print(f"Distance from CCAFS LC-40 to nearest highway: {distance_highway:.2f} km")
print(f"Distance from CCAFS LC-40 to nearest coastline: {distance_coastline:.2f} km")

"""Now, let's visualize these distances on a map. We will add markers for these proximity points and draw lines from the launch site to each proximity point."""

distances_map = folium.Map(location=[launch_site_lat, launch_site_lon], zoom_start=12)

folium.Marker(
    [launch_site_lat, launch_site_lon],
    popup='CCAFS LC-40 Launch Site',
    icon=DivIcon(
        icon_size=(20,20),
        icon_anchor=(0,0),
        html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % 'LC-40',
    )
).add_to(distances_map)

city_marker = folium.Marker(
    [city_lat, city_lon],
    popup=f'Cocoa Beach ({distance_city:.2f} km)',
    icon=folium.Icon(color='blue')
).add_to(distances_map)

folium.PolyLine(
    [[launch_site_lat, launch_site_lon], [city_lat, city_lon]],
    color='blue',
    weight=2.5,
    opacity=1
).add_to(distances_map)

railway_marker = folium.Marker(
    [railway_lat, railway_lon],
    popup=f'Nearest Railway ({distance_railway:.2f} km)',
    icon=folium.Icon(color='green')
).add_to(distances_map)

folium.PolyLine(
    [[launch_site_lat, launch_site_lon], [railway_lat, railway_lon]],
    color='green',
    weight=2.5,
    opacity=1
).add_to(distances_map)

highway_marker = folium.Marker(
    [highway_lat, highway_lon],
    popup=f'Nearest Highway ({distance_highway:.2f} km)',
    icon=folium.Icon(color='purple')
).add_to(distances_map)

folium.PolyLine(
    [[launch_site_lat, launch_site_lon], [highway_lat, highway_lon]],
    color='purple',
    weight=2.5,
    opacity=1
).add_to(distances_map)

coastline_marker = folium.Marker(
    [coastline_lat, coastline_lon],
    icon=DivIcon(
        icon_size=(20,20),
        icon_anchor=(0,0),
        html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % "{:10.2f} KM".format(distance_coastline),
    )
).add_to(distances_map)

folium.PolyLine(
    [[launch_site_lat, launch_site_lon], [coastline_lat, coastline_lon]],
    color='orange',
    weight=2.5,
    opacity=1
).add_to(distances_map)

distances_map

coordinates = [[launch_site_lat, launch_site_lon], [coastline_lat, coastline_lon]]
lines = folium.PolyLine(locations=coordinates, weight=1, color='red')

site_map.add_child(lines)
site_map
