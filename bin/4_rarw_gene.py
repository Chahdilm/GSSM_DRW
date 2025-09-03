
import os
import time
import sys

import pandas as pd
import numpy as np

import argparse

import networkx as nx


from bin.path_variable import (
    PATH_OUTPUT_FOLDER_RW,
    PATH_OUTPUT_FOLDER_MATRIX_ADD_PATIENT,
)
 
#####################################################################################""
## Parse command-line arguments
parser = argparse.ArgumentParser()

parser.add_argument(
    "--mm_type",
    required=True,
    help="Filename of the base MM matrix (e.g. mm_1_1_1_1_1)",
)
parser.add_argument(
    "--mp_type",
    required=True,
    help="Prefix of the similarity-measure files between patient and M(rd) (e.g. mp_3_2_2_2_1)",
)
parser.add_argument(
    "--seed",
    required=True,
    help="Patient ID (e.g. P0001068)",
)
parser.add_argument(
    "--alpha",
    required=True,
    help="Restart probability for PageRank (e.g. 0.3)",
    type=float,
)

args = parser.parse_args()

mp_type        = args.mp_type
mm_type        = args.mm_type
seeds = args.seed
alpha = float(args.alpha)   

#################################################################################### 


# ------------------- Paramètres de run -------------------
# mm_type="mm_1_1_1_1_1" #'mm_1_1_1_1_1' #mm_3_2_2_2_1
# mp_type = "mp_3_2_2_2_1"  # 'mp_1_1_1_1_1' # 'mp_3_2_2_2_1'
mm_type_without_mm = mm_type.replace("mm_","")
config_output = f"{mm_type}_{mp_type}"

# seeds = ['P0001068']
first_seed = seeds

# alpha=0.3


 

# -------------- Test folder  ------------------------
# Ensure output directory for RW results exists
os.makedirs(PATH_OUTPUT_FOLDER_RW, exist_ok=True)

# Directory where per-patient matrices are stored
# matrix_dir = f"/home/maroua/Bureau/my_pipeline_v3/GSSM_DRW/output/mm_sm/{mp_type}/patient_added/{mm_type_without_mm}/"
matrix_dir = f"{PATH_OUTPUT_FOLDER_MATRIX_ADD_PATIENT}/{mm_type_without_mm}/"
# Directory where patient matrices for RW will be stored
path_rw_patient =os.path.join(PATH_OUTPUT_FOLDER_RW,str(alpha),config_output)
os.makedirs(path_rw_patient, exist_ok=True)


# -------------- Test if the seed is already processed --------------
list_patient_already = os.listdir(path_rw_patient)
for onep in list_patient_already:
    onep_not_ext = onep.split('.')[0]
    if first_seed == onep_not_ext:
        print("patient already done")
        exit(0)

print("Patient start : ")

 

# -------------- Charger matrice (maladies + patient ajouté) --------------
df_m = pd.read_csv(
    os.path.join(matrix_dir, f"{first_seed}.csv"),
    index_col=0
)
 

# -------------- Build NetworkX graph and normalize--------------
G_raw = nx.from_pandas_adjacency(df_m)
G_raw.remove_edges_from(nx.selfloop_edges(G_raw))
A = nx.adjacency_matrix(G_raw)
df_adj = pd.DataFrame(
    A.toarray(),
    index=df_m.index,
    columns=df_m.columns
)
df_adj['tot'] = df_adj.sum(axis=1)

## Normalization each row tot value = 1
df_norm = (
    df_adj
    .div(df_adj['tot'], axis=0)
)

df_norm.drop(columns=['tot'],inplace=True)

 



#######################################################################""

# -------------- PageRank personnalisé (seed = patient) --------------
G = nx.from_pandas_adjacency(df_norm)
# Build personalization one hot vector 
personalization = {n: (1 if n == first_seed else 0) for n in G.nodes()}

# Precompute sum of normalized degrees
sum_degres = df_norm.sum().sort_values(ascending=False)

t0 = time.perf_counter()

# Run PageRank once per alpha
pr = nx.pagerank(G, personalization=personalization, alpha=alpha)
pr.pop(first_seed, None)

 
# nb de gènes partagés avec le patient
# nb_shared = {d: len(genes_patient & genes_by_disease.get(d, set())) for d in disease_nodes}
 
# Build result DataFrame
df_pr = (
    pd.Series(pr, name='pg')
    .to_frame()
    .assign(
        sum_degres=lambda df: df.index.map(sum_degres),
         )
)
df_pr['rank_pg'] = df_pr['pg'].rank(ascending=False, method='min')
df_pr['rank_sum_degres_pg'] = df_pr['sum_degres'].rank(ascending=False, method='min')
# Option : un rang "gene-aware" (priorité aux maladies partageant ≥1 gène, puis score PR)
 
 
out_path = os.path.join(
    PATH_OUTPUT_FOLDER_RW,
    str(alpha),       
    config_output,
    f"{first_seed}.xlsx")
df_pr.to_excel(out_path, engine='openpyxl')

print(f"{first_seed} done in {time.perf_counter() - t0:.1f}s")

