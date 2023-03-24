"""
This is a boilerplate pipeline 'inference'
generated using Kedro 0.18.6
"""

from kedro.pipeline import Pipeline, node
from kedro.pipeline.modular_pipeline import pipeline

from srai_kedro.pipelines.inference.nodes import embed


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=embed,
            name="generate_embeddings",
            inputs=["embedder", "regions_concat", "roads_concat", "joint"],
            outputs="embeddings",
        )
    ])
