import csv

from create_RES_maps import PlotRES
import logging

with open("create_maps/renewable_maps/sylvera_res_projects.csv", "r") as csvfile:
    reader = csv.DictReader(csvfile, delimiter=",")

    for data in reader:  # first loop finds project in CSV and extracts country
        project_name = data["Project ID"]
        logging.info(
            "------------------------------------\ngenerating for",
            project_name,
            "...\n",
        )
        PlotRES(project_name)
