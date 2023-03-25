"""
This is a boilerplate pipeline 'visualizations'
generated using Kedro 0.18.7
"""

from kedro.pipeline import Pipeline, node
from kedro.pipeline.modular_pipeline import pipeline

from .nodes import (
    scale_embeddings,
    generate_clustering_model,
    generate_linkage_matrix,
    plot_dendrogram,
    cluster_regions,
    plot_clustered_regions_with_roads,
)


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=scale_embeddings,
                name="scale_embeddings",
                inputs=["embeddings"],
                outputs="embeddings_scaled",
            ),
            node(
                func=generate_clustering_model,
                name="generate_clustering_model",
                inputs=["embeddings_scaled", "params:clustering"],
                outputs="clustering_model",
            ),
            node(
                func=generate_linkage_matrix,
                name="generate_linkage_matrix",
                inputs=["clustering_model"],
                outputs="linkage_matrix",
            ),
            node(
                func=plot_dendrogram,
                name="plot_dendrogram",
                inputs=["linkage_matrix", "params:dendrogram"],
                outputs="dendrogram_plot",
            ),
            node(
                func=cluster_regions,
                name="cluster_regions",
                inputs=[
                    "linkage_matrix",
                    "embeddings",
                    "regions_concat",
                    "params:clustering.clusters",
                ],
                outputs="regions_clustered",
            ),
            node(
                func=plot_clustered_regions_with_roads,
                name="plot_clustered_regions_with_roads",
                inputs=[
                    "regions_clustered",
                    "roads_concat",
                    "areas",
                    "params:clustering.clusters",
                ],
                outputs="regions_clustered_plots",
            ),
        ]
    )
