import json
import os

import geopandas as gpd
import matplotlib.pyplot as plt

"""reading files"""


def read_files(project_country):

    # make dictionary 'dir' using file_directory.py
    with open("config-tower.json") as director:
        dir = director.read()
        dir = json.loads(dir)
    # loading in countries
    countries_path = os.path.join(
        dir["other_shapefiles_dir"],
        "ne_10m_admin_0_countries",
        "ne_10m_admin_0_countries.shp",
    )
    countries = gpd.read_file(countries_path)

    # loading in rivers
    rivers_path = os.path.join(
        dir["other_shapefiles_dir"],
        "ne_10m_rivers_lake_centerlines",
        "ne_10m_rivers_lake_centerlines.shp",
    )
    rivers = gpd.read_file(rivers_path)

    # loading in lakes
    lakes_path = os.path.join(
        dir["other_shapefiles_dir"], "ne_10m_lakes", "ne_10m_lakes.shp"
    )
    lakes = gpd.read_file(lakes_path)

    # loading in oceans
    oceans_path = os.path.join(
        dir["other_shapefiles_dir"], "ne_10m_ocean", "ne_10m_ocean.shp"
    )
    oceans = gpd.read_file(oceans_path)

    # loading in state boundaries
    states_path = os.path.join(
        dir["other_shapefiles_dir"],
        "ne_10m_admin_1_states_provinces_lines",
        "ne_10m_admin_1_states_provinces_lines.shp",
    )
    states = gpd.read_file(states_path)

    # loading in legend
    map_legend_path = os.path.join(
        "renewable_maps", "renewable_icons", "map_legend.png"
    )
    map_legend = plt.imread(map_legend_path)

    return countries, rivers, lakes, oceans, states, map_legend
