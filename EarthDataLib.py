morocco_min_lon, morocco_min_lat, morocco_max_lon, morocco_max_lat = -17.10464433, 20.76691315, -1.03199947, 35.92651915
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import box

# Load the global boundaries shapefile into a GeoDataFrame
global_boundaries_gdf = gpd.read_file("./Data/GeoData/SHP/ne_10m_admin_0_countries_mar.shp")

# Filter the GeoDataFrame to extract only Morocco's boundaries
morocco_boundaries_gdf = global_boundaries_gdf[global_boundaries_gdf['NAME'] == 'Morocco']

# Calculate the minimal bounding box coordinates for Morocco
morocco_minimal_bounds = morocco_boundaries_gdf.total_bounds  # Returns (minx, miny, maxx, maxy)

# Create a rectangular polygon from the bounding box coordinates
morocco_bounding_box_polygon = box(*morocco_minimal_bounds)

# Create a new GeoDataFrame for the bounding box to enable plotting
bounding_box_gdf = gpd.GeoDataFrame(geometry=[morocco_bounding_box_polygon], crs=morocco_boundaries_gdf.crs)

# Plotting
fig, ax = plt.subplots(figsize=(10, 10))
# Plot Morocco's boundaries
morocco_boundaries_gdf.plot(ax=ax, color="lightblue", edgecolor='k', linewidth=1, label='Morocco')
# Plot the bounding box
bounding_box_gdf.boundary.plot(ax=ax, color="red", linestyle='--', linewidth=2, label='Bounding Box')

# Enhance the plot
ax.set_title('Morocco and its Minimal Bounding Box')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
plt.legend()

# Show the plot
plt.show()

# Print the minimal bounding box coordinates
print(f"Minimal Bounding Box for Morocco: {morocco_minimal_bounds}")



import geopandas as gpd
from shapely.geometry import Point


# Assuming world is already loaded as a GeoDataFrame
world = gpd.read_file("./Data/GeoData/SHP/ne_10m_admin_0_countries_mar.shp")

def filter_points_within_morocco(df):
    """
    Filter rows based on whether their point locations fall within Morocco.

    Args:
    df (pd.DataFrame): A DataFrame containing 'Latitude' and 'Longitude' columns.

    Returns:
    gpd.GeoDataFrame: A GeoDataFrame containing only the rows where points are within Morocco.
    """
    # Ensure the input DataFrame has 'Latitude' and 'Longitude' columns
    if not {'Latitude', 'Longitude'}.issubset(df.columns):
        raise ValueError("DataFrame must contain 'Latitude' and 'Longitude' columns")

    # Convert the DataFrame to a GeoDataFrame, setting the geometry from Latitude and Longitude
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.Longitude, df.Latitude))

    # Filter the world GeoDataFrame to include only Morocco
    morocco = world[world['ADMIN'] == 'Morocco'].geometry.iloc[0]

    # Filter rows where geometry is within Morocco
    gdf_within_morocco = gdf[gdf.geometry.within(morocco)]

    return gdf_within_morocco

# Example usage:
# Assuming you have a DataFrame `df` with 'Latitude' and 'Longitude'
# df_within_morocco = filter_points_within_morocco(df)
# print(df_within_morocco)
