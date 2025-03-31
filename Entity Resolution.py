import pandas as pd
import re
from rapidfuzz import fuzz
import networkx as nx

def normalize_name(name):
    if pd.isnull(name):
        return ""
    name = name.lower()
    name = re.sub(r"[^a-z0-9\s]", "", name)
    name = re.sub(r"\s+", " ", name)
    return name.strip()

df = pd.read_parquet("veridion_entity_resolution_challenge.snappy.parquet", engine="pyarrow")

df["normalized_name"] = df["company_name"].apply(normalize_name)

blocks = {}
for idx, row in df.iterrows():
    key = row["normalized_name"][0] if row["normalized_name"] else ""
    blocks.setdefault(key, []).append(idx)

threshold = 90
G = nx.Graph()
G.add_nodes_from(df.index)
for block_key, indices in blocks.items():
    for i in range(len(indices)):
        for j in range(i + 1, len(indices)):
            idx_i, idx_j = indices[i], indices[j]
            name_i = df.loc[idx_i, "normalized_name"]
            name_j = df.loc[idx_j, "normalized_name"]
            similarity = fuzz.token_sort_ratio(name_i, name_j)
            if similarity >= threshold:
                G.add_edge(idx_i, idx_j)

groups = {}
for group_id, component in enumerate(nx.connected_components(G)):
    for idx in component:
        groups[idx] = group_id

df["company_group_id"] = df.index.map(groups)

print(df[["company_name", "company_group_id"]].head())
