## Analysis of HPO to SNOMED CT mappings

### Setup
The code requires a `hpo.obo` file with the HPO in OBO format placed at the `data/01_raw` folder. This can be downloaded from the [HPO Web site](https://hpo.jax.org/data/ontology).

### Preparation

The first step is running `1_extract_annotate.py` that takes the HPO ontology, extract the supgraph of anomalies, adds annotations and then saves the subgraph as a compressed GML file. 

### Analytics




### Additional info

#### Detailed mappings to SNOMED
See applicable attributes in SNOMED CT https://browser.ihtsdotools.org/mrcm/?branch=MAIN%2F2025-04-01
Detailed mappings to SNOMED CT expressions: https://confluence.ihtsdotools.org/display/CC/HPO+to+SNOMED+mapping
Video about the mappings: https://www.youtube.com/watch?v=d_4QPmTBtfs 