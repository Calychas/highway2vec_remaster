"""
This is a boilerplate pipeline 'processing'
generated using Kedro 0.18.6
"""

from kedro.pipeline import Pipeline, node
from kedro.pipeline.modular_pipeline import pipeline
from .nodes import download_areas, regionize_areas, download_road_infrastructure, concat_partitioned_dataset, generate_joint_features_with_regions

from srai.constants import FEATURES_INDEX

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=download_areas,
                name="download_areas",
                inputs=["cities"],
                outputs="areas",
            ),
            node(
                func=regionize_areas,
                name="regionize_areas",
                inputs=["areas", "params:resolution"],
                outputs="regions",
            ),
            node(
                func=download_road_infrastructure,
                name="download_road_infrastructure",
                inputs=["areas", "params:network_type"],
                outputs=["intersections", "roads"],
            ),
            node(
                func=concat_partitioned_dataset,
                name="concat_regions",
                inputs=["regions"],
                outputs="regions_concat",
            ),
            node(
                func=concat_partitioned_dataset,
                name="concat_intersections",
                inputs=["intersections"],
                outputs="intersections_concat",
            ),
            node(
                func=lambda x: concat_partitioned_dataset(x, FEATURES_INDEX),
                name="concat_roads",
                inputs=["roads"],
                outputs="roads_concat",
            ),
            node(
                func=generate_joint_features_with_regions,
                name="join_roads_with_regions",
                inputs=["roads_concat", "regions_concat"],
                outputs="joint",
            )
        ]
    )
