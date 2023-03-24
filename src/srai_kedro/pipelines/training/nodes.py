"""
This is a boilerplate pipeline 'training'
generated using Kedro 0.18.6
"""
from typing import Dict, Any

import geopandas as gpd
from srai.embedders import Highway2VecEmbedder
from pytorch_lightning import seed_everything
import mlflow

def train(regions_gdf: gpd.GeoDataFrame, features_gdf: gpd.GeoDataFrame, joint_gdf: gpd.GeoDataFrame, trainer_params: Dict[str, Any], dataloader_params: Dict[str, Any]) -> Highway2VecEmbedder:
    seed_everything(42)
    
    mlflow.pytorch.autolog()
    embedder = Highway2VecEmbedder()
    embedder.fit(regions_gdf, features_gdf, joint_gdf, trainer_kwargs=trainer_params, dataloader_kwargs=dataloader_params)
    return embedder