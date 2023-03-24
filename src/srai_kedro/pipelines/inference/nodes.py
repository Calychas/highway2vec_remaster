"""
This is a boilerplate pipeline 'inference'
generated using Kedro 0.18.6
"""

from srai.embedders import Highway2VecEmbedder
import pandas as pd
import geopandas as gpd

def embed(embedder: Highway2VecEmbedder, regions_gdf: gpd.GeoDataFrame, features_gdf: gpd.GeoDataFrame, joint_gdf: gpd.GeoDataFrame) -> pd.DataFrame:
    embeddings = embedder.transform(regions_gdf, features_gdf, joint_gdf)
    return embeddings