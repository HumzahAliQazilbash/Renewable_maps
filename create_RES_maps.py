import csv
import os
from glob import glob

import geopandas as gpd
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image
from renewable_maps.create_extent import create_extent_from_shp
from renewable_maps.mapsetup import read_files
from shapely.geometry import Point
import logging

logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger("renewable_maps")

class PlotRES:
    def __init__(self, project, run_location: bool = True):
        self.project = project
        self.run_location = run_location

        csvfile = open("renewable_maps/res_projects.csv", "r", encoding="utf8")
        reader = csv.DictReader(csvfile, delimiter=",")
        self.reader = reader
        self.csvfile = csvfile

    def extract_country_time(self):
        logger.info("extracting country of the project and start year")
        for data in self.reader:  # first loop finds project in CSV and extracts country
            if self.project == data["Project ID"]:
                self.project_country = data["Country"]
                if data["First Year of Project"] != "":
                    self.project_time = int(float(data["First Year of Project"]))
                else:
                    logger.info("no start date for project, setting it to 0")
                    self.project_time = 0
                logger.info("country of the project and start year extracted")
                return self.project_country, self.project_time

    def add_to_dict(self):
        logger.info("adding country RES data to appropriate dicts")
        for (
            data
        ) in self.reader:  # 2nd loop will go through data and load them into lists
            if data["Country"] == self.project_country:
                if data["long"] != "":
                    data["long"] = float(data["long"])
                    data["lat"] = float(data["lat"])
                    if (
                        data["Type"]
                        not in (
                            "Hydropower",
                            "Wind",
                            "Solar - Centralized",
                            "Geothermal",
                            "RE Bundled",
                            "Biomass",
                        )
                        and data["Project ID"] == self.project
                    ):
                        logger.info(
                            "project does not have recognised type:(, skipping..."
                        )
                        return

                    elif data["Project ID"] == self.project:
                        self.project_dict.append(data)

                    else:
                        if data["Type"] == "Wind":
                            self.wind_dict.append(data)

                        elif data["Type"] == "Hydropower":
                            self.hydropower_dict.append(data)

                        elif data["Type"] == "Solar - Centralized":
                            self.solar_dict.append(data)

                        elif data["Type"] == "Geothermal":
                            self.geothermal_dict.append(data)

                        elif data["Type"] == "RE Bundled":
                            self.bundled_dict.append(data)

                        elif data["Type"] == "Biomass":
                            self.biomass_dict.append(data)

                        else:
                            continue

                # DICTIONARY LISTS -> GEODATFRAME -> PLOT POINTS

    def dict_to_gdf(self, dictionary_series, project_type):
        if len(dictionary_series) < 1:
            logger.info(
                f"no data available in {self.project_country} for {project_type}",
            )
            return
        else:
            if self.project_country == "India":
                marker_size = 15
            else:
                marker_size = 25

            df = pd.DataFrame(dictionary_series)
            geometry = [Point(xy) for xy in zip(df.long, df.lat)]
            df = df.drop(["long", "lat"], axis=1)
            gdf = gpd.GeoDataFrame(df, crs="EPSG:4326", geometry=geometry)
            project_colors = {
                "wind": "#8F8CFF",
                "hydropower": "#68E4FF",
                "solar": "#ff8b47",
                "geothermal": "#F20C59",
                "bundled": "#474747",
                "biomass": "#2ECB50",
            }
            plotting_color = project_colors[project_type]
            logger.info(f"plotting data for {project_type}")
            gdf.plot(
                ax=self.ax, color=plotting_color, zorder=20, markersize=marker_size
            )

    def proj_to_gdf(self, dictionary_series, project_type):
        if len(dictionary_series) < 1:
            logger.info(
                f"no data available in {self.project_country} for {project_type}"
            )
            return
        else:
            self.project_type = dictionary_series[0]["Type"]
            imagewidth = (
                abs(self.xlim[1] - self.xlim[0])
            ) / 35  # divider determines width and height of icon

            x0 = dictionary_series[0]["long"]
            x1 = x0 + imagewidth
            y0 = dictionary_series[0]["lat"]
            y1 = y0 + imagewidth

            icon_path = glob(
                os.path.join(
                    "renewable_icons",
                    self.project_type,
                    "*.png",
                )
            )
            plt.imshow(
                plt.imread(icon_path[0]),
                extent=(x0, x1, y0, y1),
                zorder=30,
                alpha=0.9,
            )

            logger.info(f"extent is {x0} {x1} {y0} {y1}")

            # project annotation
            annotation_pad = imagewidth / 2
            plt.annotate(
                dictionary_series[0]["Project ID"],
                xy=(x0, y0 - (annotation_pad)),
                alpha=0.8,
                zorder=22,
                size=12,
                family="DejaVu Sans",
                bbox=dict(
                    facecolor="white",
                    alpha=0.5,
                    edgecolor="none",
                    boxstyle="round,pad=0.5",
                ),
            )
            plt.annotate(
                dictionary_series[0]["Project ID"],
                xy=(x0, y0 - (annotation_pad)),
                alpha=0.8,
                zorder=22,
                size=12,
                family="DejaVu Sans",
                bbox=dict(
                    facecolor="none",
                    edgecolor="black",
                    linewidth=0.3,
                    boxstyle="round,pad=0.5",
                ),
            )

    def export_plot(self):
        output_dir_local = "outputs"
        if not os.path.exists(output_dir_local):
            os.makedirs(output_dir_local)
        output_fp = f"{output_dir_local}/{self.project}_RESProjectMap.jpeg"
        # outputs_rem = output_dir_local.split("/")[:-1]
        # outputs_rem = "/".join(outputs_rem)
        

        plt.savefig(
            f"{output_fp}",
            dpi=300,
            bbox_inches="tight",
        )
        image = Image.open(f"{output_fp}")
        resized_image = image.resize((2048, 1350))
        resized_image.save(f"{output_fp}")
        plt.clf()
        plt.close("all")
        logger.info(f"plotting and export for {self.project} successful")
        return

    def main(self):
        try:
            project_country, project_time = self.extract_country_time()
        except TypeError:
            projectid = str(input("please re-enter project id : "))
            try:
                project_country, project_time = self.extract_country_time()
            except:
                raise ValueError("please check project id")
                

        logger.info(f"project in {project_country} starting in {project_time}")

        # adding csv data to dictionary lists
        (
            self.project_dict,
            self.hydropower_dict,
            self.wind_dict,
            self.solar_dict,
            self.geothermal_dict,
            self.bundled_dict,
            self.biomass_dict,
        ) = ([], [], [], [], [], [], [])

        self.csvfile.seek(0)

        self.add_to_dict()
        # LOADING FILES FROM mapsetup.py

        countries, rivers, lakes, oceans, states, map_legend = read_files(
            project_country
        )  # reads files from mapsetup

        # AXIS SETUP
        # checking if project_country is in countries_admin_0.shp
        countries_list = countries["ADMIN"].tolist()
        if project_country not in countries_list:
            logger.info(f"ADMIN.shp_ERROR {project_country} not found in shapefile")
            return

        # setting the limits of the axes using extent shp
        country_shp = countries.loc[
            countries["ADMIN"] == project_country
        ]  # makes a gdf based on project country
        xlim, ylim, legend_extent = create_extent_from_shp(country_shp)

        # create axis for plotting image
        my_dpi = 1000
        fig, ax = plt.subplots(figsize=(22133 / my_dpi, 14590 / my_dpi), dpi=my_dpi)

        # cropping axis to limits from extent shp
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
        ax.set_axis_off()
        # AXIS OFF

        self.ax = ax
        self.ylim = ylim
        self.xlim = xlim

        # PLOTTING SHAPEFILES

        # plot land shapefile
        countries.plot(ax=ax, color="#EFEFEF", alpha=1)

        # plot all rivers
        rivers.plot(ax=ax, color="#acf6fa", linewidth=0.5, zorder=9)

        # plot country boundary
        country_shp.plot(ax=ax, facecolor="#F9F9F9", zorder=5)
        country_shp.plot(
            ax=ax, facecolor="none", edgecolor="black", linewidth=0.2, zorder=20
        )

        # plot all oceans
        oceans.plot(ax=ax, color="#acf6fa")

        # plot all lakes
        lakes.plot(ax=ax, color="#acf6fa")

        # plot the source
        plt.text(
            xlim[0] + (xlim[1] - xlim[0]) / 100,
            ylim[0] + (ylim[1] - ylim[0]) / 80,
            "Source: Verra VCS Registry",
            fontdict={"family": "DejaVu Sans", "color": "#424177", "size": 14},
        )

        # plotting xy data
        self.proj_to_gdf(self.project_dict, "project")
        self.dict_to_gdf(self.wind_dict, "wind")
        self.dict_to_gdf(self.hydropower_dict, "hydropower")
        self.dict_to_gdf(self.solar_dict, "solar")
        self.dict_to_gdf(self.geothermal_dict, "geothermal")
        self.dict_to_gdf(self.biomass_dict, "biomass")
        self.dict_to_gdf(self.bundled_dict, "bundled")

        # plotting legend
        ax.imshow(map_legend, extent=legend_extent, zorder=25, alpha=1)

        """------SAVING AND RESIZING IMAGE-----------"""
        self.export_plot()

        return

projectid = str(input("Enter the project id : "))
run = PlotRES(projectid)
run.main()