"""
This is a boilerplate pipeline 'training'
generated using Kedro 0.18.6
"""

from kedro.pipeline import Pipeline, node
from kedro.pipeline.modular_pipeline import pipeline

from srai_kedro.pipelines.training.nodes import train


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=train,
            name="train_embedder",
            inputs=["regions_concat", "roads_concat", "joint", "params:trainer_params", "params:dataloader_params"],
            outputs="embedder",
        )
    ])
