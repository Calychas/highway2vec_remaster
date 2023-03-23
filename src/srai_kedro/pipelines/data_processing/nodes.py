"""
This is a boilerplate pipeline 'data_processing'
generated using Kedro 0.18.6
"""
from typing import Callable, Dict, Tuple
import pandas as pd
import geopandas as gpd
from tqdm.auto import tqdm
from srai.utils import geocode_to_region_gdf
from srai.loaders import OSMWayLoader
from srai.loaders.osm_way_loader import NetworkType
from srai.regionizers import H3Regionizer
import unidecode


LazyLoadedGeoDataFrames = Dict[str, Callable[[], gpd.GeoDataFrame]]


def get_place_dir_name(place_name: str) -> str:
    return "_".join(
        unidecode.unidecode(place_name)
        .replace(",", "_")
        .replace(" ", "-")
        .split("_")[0:2]
    )


def download_areas(cities_df: pd.DataFrame) -> LazyLoadedGeoDataFrames:
    filtered_cities_df = cities_df[
        (cities_df["country"] == "Poland") & (cities_df["regions"].isna())
    ]

    cities_to_download: LazyLoadedGeoDataFrames = {}
    for row in filtered_cities_df.itertuples():
        place_name = f"{row.city},{row.country}"
        cities_to_download[
            get_place_dir_name(place_name)
        ] = lambda x=place_name: geocode_to_region_gdf(x)

    return cities_to_download


def regionize_areas(areas: LazyLoadedGeoDataFrames) -> LazyLoadedGeoDataFrames:
    regionizer = H3Regionizer(9)

    regions = {}
    for area_name, area_func in areas.items():
        area_gdf = _load_gdf(area_func)

        regions_df = regionizer.transform(area_gdf)
        regions[area_name] = regions_df

    return regions


def download_road_infrastructure(
    areas: LazyLoadedGeoDataFrames,
) -> Tuple[LazyLoadedGeoDataFrames, LazyLoadedGeoDataFrames]:
    loader = OSMWayLoader(NetworkType.DRIVE)

    intersections = {}
    roads = {}
    for area_name, area_func in areas.items():
        area_gdf = _load_gdf(area_func)
        gdf_n, gdf_e = loader.load(area_gdf)

        intersections[area_name] = gdf_n
        roads[area_name] = gdf_e

    return intersections, roads


def concat_partitioned_dataset(partitioned_dataset: LazyLoadedGeoDataFrames) -> gpd.GeoDataFrame:
    return pd.concat([_load_gdf(d) for d in partitioned_dataset.values()])


def _load_gdf(gdf_func: Callable[[], gpd.GeoDataFrame]) -> gpd.GeoDataFrame:
    gdf = gdf_func()
    gdf = gpd.GeoDataFrame(
        geometry=gpd.GeoSeries.from_wkb(gdf.geometry), index=gdf.index, crs="epsg:4326"
    )

    return gdf
