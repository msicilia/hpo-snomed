"""_summary_
    Extracts the abnormal subgraph from HPO and annotates its nodes with useful information.
    Writes the resulting graph to an intermediate GML file.
"""
import obonet
import networkx as nx
from util import get_abnormal_subgraph, annotate_nodes
from pathlib import Path

RAW_DATA_FOLDER = Path("data/01_raw")
INTERMEDIATE_DATA_FOLDER = Path("data/02_intermediate")

# Read the ontology and extract the abnormal subgraph
hpo = obonet.read_obo(RAW_DATA_FOLDER / "hp.obo")
abnormal = get_abnormal_subgraph(hpo)
print(f"Total abnormal nodes: {len(abnormal)} out of a total of {len(hpo)} nodes in HPO")

# Annotate nodes with useful information
abnormal = annotate_nodes(abnormal)

# Write to GML file.
# Fix keys in graph attributes to be compatible with GML format
for key in list(abnormal.graph.keys()):
    new_key = key.replace("-", "_")
    if new_key != key:
        abnormal.graph[new_key] = abnormal.graph[key]
        del abnormal.graph[key]
nx.write_gml(abnormal, INTERMEDIATE_DATA_FOLDER / "abnormal.gml.gz")

# Sanity check for the reading.
G = nx.read_gml(INTERMEDIATE_DATA_FOLDER / "abnormal.gml.gz")
print(G.nodes["HP:0010281"])
