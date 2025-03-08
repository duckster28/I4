import pandas as pd
import folium
from folium.plugins import HeatMap

# Load the dataset
file_path = 'University_Dataset(tmc_raw_data_2020_2029).csv'
df = pd.read_csv(file_path)

# Sum up throughput for each mode
df['total_cars'] = df[
    ['n_appr_cars_r', 'n_appr_cars_t', 'n_appr_cars_l',
     's_appr_cars_r', 's_appr_cars_t', 's_appr_cars_l',
     'e_appr_cars_r', 'e_appr_cars_t', 'e_appr_cars_l',
     'w_appr_cars_r', 'w_appr_cars_t', 'w_appr_cars_l']
].sum(axis=1)

df['total_buses'] = df[
    ['n_appr_bus_r', 'n_appr_bus_t', 'n_appr_bus_l',
     's_appr_bus_r', 's_appr_bus_t', 's_appr_bus_l',
     'e_appr_bus_r', 'e_appr_bus_t', 'e_appr_bus_l',
     'w_appr_bus_r', 'w_appr_bus_t', 'w_appr_bus_l']
].sum(axis=1)

df['total_pedestrians'] = df[['n_appr_peds', 's_appr_peds', 'e_appr_peds', 'w_appr_peds']].sum(axis=1)
df['total_bikes'] = df[['n_appr_bike', 's_appr_bike', 'e_appr_bike', 'w_appr_bike']].sum(axis=1)

# Calculate total throughput
df['total_throughput'] = df[['total_cars', 'total_buses', 'total_bikes', 'total_pedestrians']].sum(axis=1)

# Aggregate by location
aggregated_df = df.groupby(['location_name', 'latitude', 'longitude'])[['total_throughput']].sum().reset_index()

# Generate a map centered around Toronto
m = folium.Map(location=[43.7, -79.4], zoom_start=12)

# Plot each intersection with throughput data
for index, row in aggregated_df.iterrows():
    folium.CircleMarker(
        location=(row['latitude'], row['longitude']),
        radius=row['total_throughput'] / 20000,  # Decrease the circle size further
        color='blue',
        fill=True,
        fill_opacity=0.5,
        popup=f"{row['location_name']}<br>Total Throughput: {row['total_throughput']}"
    ).add_to(m)

# Generate a heatmap based on throughput
heatmap_data = [[row['latitude'], row['longitude'], row['total_throughput']] for index, row in aggregated_df.iterrows()]
for index, row in aggregated_df.iterrows():
    folium.CircleMarker(
        location=(row['latitude'], row['longitude']),
        radius=row['total_throughput'] / 20000,
        color='blue',
        fill=True,
        fill_opacity=0.5,
        popup=f"{row['location_name']}<br>Total Throughput: {row['total_throughput']}"
    ).add_to(m)
HeatMap(heatmap_data, radius=25).add_to(m)

# Save the map as an HTML file
m.save('toronto_traffic_map.html')

print("✅ Map saved as 'toronto_traffic_map.html'. Open it in any browser.")
