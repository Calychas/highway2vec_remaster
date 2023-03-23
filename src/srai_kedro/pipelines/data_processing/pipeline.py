"""
This is a boilerplate pipeline 'data_processing'
generated using Kedro 0.18.6
"""

from kedro.pipeline import Pipeline, node
from kedro.pipeline.modular_pipeline import pipeline
from .nodes import download_areas, regionize_areas, download_road_infrastructure, concat_partitioned_dataset


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
                inputs=["areas"],
                outputs="regions",
            ),
            node(
                func=download_road_infrastructure,
                name="download_road_infrastructure",
                inputs=["areas"],
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
                name="concat_roads",
                inputs=["roads"],
                outputs="roads_concat",
            )
        ]
    )
