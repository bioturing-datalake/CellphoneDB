import os
from fastapi import FastAPI
from utils import db_utils, search_utils
from fastapi.middleware.cors import CORSMiddleware

RELEASED_VERSION="v5.0.0"
CPDB_ROOT = os.path.join(os.path.expanduser('~'),".cpdb")

interactions, genes, complex_composition, complex_expanded = \
    db_utils.get_interactions_genes_complex(CPDB_ROOT, RELEASED_VERSION)

app = FastAPI()

# See: https://fastapi.tiangolo.com/tutorial/cors/
origins = [
    "http://localhost:8001"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
)

# Return cpdb version
@app.get("/dbversion")
def read_root():
    return {"dbversion": RELEASED_VERSION}

# Search for interactions using space- or comma-separated list of terms in {tokens}
@app.get("/search/{tokens}")
def find_interactions(tokens: str):
    results, complex_name2proteins_text = search_utils.search(tokens, CPDB_ROOT, RELEASED_VERSION)
    return {"results_html_table" : search_utils.get_html_table(results, complex_name2proteins_text) }

# Autocomplete {partial_element} using data in genes table or complex names in interactions table
@app.get("/autocomplete/{partial_element}")
def autocomplete(partial_element: str):
    matches_list = search_utils.autocomplete_query(genes, interactions, partial_element)["value"].tolist()
    return { "matches" : matches_list }

# Return all gene, protein and complex ids in cpdb
@app.get("/all_ids")
def get_all_ids():
    all_ids = search_utils.return_all_identifiers(genes, interactions)["value"].tolist()
    return { "all_ids" : all_ids }