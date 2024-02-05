import logging


def create_extent_from_shp(proj_shp):
    """AXIS SETUP"""
    # setting the limits of the axes using extent shp
    xshape = proj_shp.total_bounds[2] - proj_shp.total_bounds[0]
    yshape = proj_shp.total_bounds[3] - proj_shp.total_bounds[1]

    # determine how much padding, higher the divider the less padding there will be
    ydivider = 20
    xdivider = 6
    if yshape > ((xshape * (1 + 2 / ydivider)) / 1.517):
        logging.info("setting bbox based on y coordinates...")
        y_pad = yshape / ydivider
        ylim = (
            proj_shp.total_bounds[1] - y_pad,
            proj_shp.total_bounds[3] + y_pad,
        )  # adds padding below and above shp

        x_length = (
            yshape * (1 + 2 / ydivider) * 1.517
        )  # multiply by 3/2 to include padding and 1.517 is aspect ratio
        x_pad = (x_length - xshape) / 2
        xlim = (proj_shp.total_bounds[0] - x_pad, proj_shp.total_bounds[2] + x_pad)
    else:
        logging.info("setting bbox based on x coordinates...")
        x_pad = xshape / xdivider
        xlim = (
            proj_shp.total_bounds[0] - x_pad,
            proj_shp.total_bounds[2] + x_pad,
        )  # adds padding below and above shp

        y_length = (
            xshape * (1 + 2 / xdivider)
        ) / 1.517  # multiply by 3/2 to include padding and 1.517 is aspect ratio
        y_pad = (y_length - yshape) / 2
        ylim = (proj_shp.total_bounds[1] - y_pad, proj_shp.total_bounds[3] + y_pad)

    # map legend
    x0 = xlim[0]
    x1 = xlim[1]
    y0 = ylim[0]
    y1 = ylim[1]
    legend_extent = (
        x1 - (abs(x1 - x0)) / 6,
        x1 - (abs(x1 - x0)) / 115,
        y1 - (abs(y1 - y0)) / 2.75,
        y1 - (abs(y1 - y0)) / 100,
    )  # adjusting legend position within bounding box
    return xlim, ylim, legend_extent
