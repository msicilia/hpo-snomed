
import obonet
import networkx as nx

ABNORMAL_HPO_ID = "HP:0000118"  # Phenotypic abnormality

def get_descendants(hpo: nx.MultiDiGraph, node_id: str) -> set[str]:
    """Returns the ids of all descendants of a given node in the HPO graph.
    Note that in the HPO graph, edges point from child to parent."""
    return nx.ancestors(hpo, node_id)

def get_abnormal_subgraph(hpo: nx.MultiDiGraph) -> nx.MultiDiGraph:
    """Gets the subgraph of all abnormality nodes (descendants of HP:0000118).
    """
    abnormal_ids = list(get_descendants(hpo, ABNORMAL_HPO_ID))
    abnormal_ids.append(ABNORMAL_HPO_ID)
    return hpo.subgraph(abnormal_ids)

def mapped_to_snomed(graph: nx.MultiDiGraph) -> tuple[list[str], list[str]]:
    """Returns the lists of node ids that are mapped to SNOMED CT and those that are not.
    """
    mapped = []
    unmapped = []
    for node_id in graph.nodes:
        node_data = graph.nodes[node_id]
        references = node_data.get('xref', [])
        if any(ref.startswith("SNOMEDCT") for ref in references):
            mapped.append(node_id)
        else:
            unmapped.append(node_id)
    return mapped, unmapped


def annotate_nodes(abnormal: nx.MultiDiGraph) -> nx.MultiDiGraph:
    """Annotates the given nodes with the provided annotation.
     Annotations:
     - "M": whether the node is mapped to SNOMED CT
     - "L": whether the node is a leaf (no children in the abnormal subgraph)
     - "shortest_path_to_abnormal_id": the shortest path from the node to HP:0000118
     - "I": whether the node is an intermediate node (not mapped, not leaf, has some mapped ancestor and some mapped descendant)
     - "T": whether the node is a terminal node (not mapped, not intermediate)
    """
    mapped, _ = mapped_to_snomed(abnormal)
    abnormal_undirected = abnormal.to_undirected(as_view=True)
    for n in abnormal:
        abnormal.nodes[n]["M"] = n in mapped
        abnormal.nodes[n]["shortest_path_to_abnormal_id"] = nx.shortest_path(abnormal_undirected, 
                                                            ABNORMAL_HPO_ID, n)
        abnormal.nodes[n]["L"] = len(nx.ancestors(abnormal, n))==0
    for p in abnormal:
        mapped_descendants = [abnormal.nodes[n]["M"] for n in nx.ancestors(abnormal, p)] 

        # not mapped non-leaves that have some mapped ancestor (this is true for all abnormal) and some mapped descendant
        abnormal.nodes[p]["I"] =   not abnormal.nodes[p]["M"] \
                               and not abnormal.nodes[p]["L"] \
                               and any( mapped_descendants ) 

        #not mapped nodes that are not intermediate.
        abnormal.nodes[p]["T"] = not abnormal.nodes[p]["M"] \
                             and not abnormal.nodes[p]["I"]
    return abnormal











def next_descendants_layer(hpo: nx.MultiDiGraph, node_ids: list[str]) -> list[str]:
    return [f for n in node_ids for f, t in hpo.in_edges(n)]

def info_for_node(hpo: nx.MultiDiGraph, node_id: str) -> dict:
    """Returns the information for a given node in the HPO graph."""
    return hpo.nodes.get(node_id, {})

