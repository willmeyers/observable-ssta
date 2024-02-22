import io
import json
import math
import logging
from datetime import datetime, timedelta
from collections import OrderedDict

import requests
from shapely import coords
import xarray as xr
import numpy as np
import geopandas as gpd
from shapely.geometry import Point, Polygon, mapping


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# You may configure these values yourself ###########
#
# Set the region of interest
LONGITUDE_MIN = -111.837959
LONGITUDE_MAX = -90.837959
LATITUDE_MIN = 13.837959
LATITUDE_MAX = 28.837959
#
# Set the start and end dates (use YYYY-MM-DD format)
START_DATE = "2023-11-21"
END_DATE = "2023-11-26"
#
#####################################################


# Base URL for fetching daily sea surface temperature NetCDF4 file from NOAA
BASE_URL = "https://www.star.nesdis.noaa.gov/pub/sod/mecb/crw/data/5km/v3.1_op/nc/v1.0/daily/ssta"


def get_domain_polygon():
    """

    Returns a ploygon of the domain (region of interest).

    """

    polygon = Polygon([
        (LONGITUDE_MIN, LATITUDE_MAX),
        (LONGITUDE_MIN, LATITUDE_MAX),
        (LONGITUDE_MAX, LATITUDE_MAX),
        (LONGITUDE_MAX, LATITUDE_MIN),
        (LONGITUDE_MIN, LATITUDE_MIN)
    ])

    geojson_domain = mapping(polygon)

    return geojson_domain


def process(formatted_date: str, content: bytes):
    """

    Processes response.

    """

    file_obj = io.BytesIO(content)
    ds = xr.open_dataset(file_obj)
    formatted_date = datetime.strptime(formatted_date, '%Y%m%d').strftime('%Y-%m-%d')

    anoms = ds["sea_surface_temperature_anomaly"]
    anoms = anoms.fillna(0)
    anoms = anoms.where(anoms != 0)
    lons, lats = np.meshgrid(ds['lon'].values, ds['lat'].values)
    lons = np.round(lons.flatten(), 3)
    lats = np.round(lats.flatten(), 3)
    anoms_values = np.round(anoms.values.flatten(), 2)

    within_square = (lons >= LONGITUDE_MIN) & (lons <= LONGITUDE_MAX) & (lats >= LATITUDE_MIN) & (lats <= LATITUDE_MAX)
    geometry = [Point(lon, lat) for lon, lat in zip(lons[within_square], lats[within_square])]
    anoms_values = anoms_values[within_square]

    gdf = gpd.GeoDataFrame({"a": anoms_values, "geometry": geometry, "date": formatted_date})
    gdf.crs = "EPSG:32663"
    gdf = gdf.to_crs("EPSG:3857")

    geojson_str = gdf.to_json(na="drop")
    geojson = json.loads(geojson_str)

    return geojson


def main():
    data = OrderedDict()

    start_date = datetime.strptime(START_DATE, "%Y-%m-%d")
    end_date = datetime.strptime(END_DATE, "%Y-%m-%d")
    delta = timedelta(days=1)

    current_date = start_date

    geojson_domain = None
    logger.info(f"Beginning processing for {start_date} - {end_date}")
    while current_date <= end_date:
        year = current_date.year
        formatted_date = current_date.strftime('%Y%m%d')
        filename = f"ct5km_ssta_v3.1_{formatted_date}.nc"
        url = f"{BASE_URL}/{year}/{filename}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            logger.info(f"Downloaded {filename} from server. Starting processing")
            computed_geojson = process(formatted_date, response.content)
            data[formatted_date] = computed_geojson
        except Exception as e:
            logger.error(f"Failed to process {filename}. Error: {e}")

        logger.info(f"Finished processing {filename}")

        current_date += delta

    data["domain"] = get_domain_polygon()

    with open("./docs/data/data.json", "w+") as f:
        final_json = json.dumps(data)
        f.write(final_json)


if __name__ == "__main__":
    main()
