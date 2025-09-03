    
 

import os
CONFIG_RD = "1_1_1_1_1_concat_matrix"
CONFIG_ALPHA = "0.1"
# Compose config string
CONFIG = f"{CONFIG_RD}_{CONFIG_ALPHA}"

# Path resolution
BIN_DIR = "/home/maroua/Bureau/my_pipeline_v3/GSSM_DRW/bin"#os.path.dirname(os.path.abspath(__file__))

PROJECT_ROOT = os.path.abspath(os.path.join(BIN_DIR, ".."))  # because path_variable is in bin folder

# Output and Input roots
PATH_OUTPUT = os.path.join(PROJECT_ROOT, "output")
PATH_INPUT = os.path.join(PROJECT_ROOT, "input")
PATH_INPUT_HPO = os.path.join(PATH_INPUT, "hpo")

# Make sure main folders exist
os.makedirs(PATH_OUTPUT, exist_ok=True)
os.makedirs(PATH_INPUT, exist_ok=True)
os.makedirs(PATH_INPUT_HPO, exist_ok=True)

# Log folder
PATH_LOG = os.path.join(PATH_OUTPUT, "log")
os.makedirs(PATH_LOG, exist_ok=True)
PATH_LOG_FILE = f"{PATH_LOG}/log_{CONFIG}.log"

# Output folders
PATH_OUTPUT_SM = os.path.join(PATH_OUTPUT, "mp_sm")
os.makedirs(PATH_OUTPUT_SM, exist_ok=True)

PATH_OUTPUT_SM_CDF_FILE = f"{PATH_OUTPUT_SM}/CDF_{CONFIG}.xlsx"

PATH_OUTPUT_MM = os.path.join(PATH_OUTPUT, "mm_sm")
os.makedirs(PATH_OUTPUT_MM, exist_ok=True)

PATH_OUTPUT_FOLDER_MATRIX_ADD_PATIENT = os.path.join(PATH_OUTPUT_MM, "patient_added")
os.makedirs(PATH_OUTPUT_FOLDER_MATRIX_ADD_PATIENT, exist_ok=True)

PATH_OUTPUT_PATIENT_SOLVERD = os.path.join(PATH_OUTPUT, "patient_solverd")
os.makedirs(PATH_OUTPUT_PATIENT_SOLVERD, exist_ok=True)
PATH_OUTPUT_DF_PATIENT_ONLY_DISORDER =f"{PATH_OUTPUT_PATIENT_SOLVERD}/patient_confirmed_solverd_only_disorder_with_ontologyX.xlsx"


# Columns (keep as string constants)
COL_DF_PATIENT_PATIENT = "phenopacket"
COL_DF_PATIENT_ORPHACODE = "Disease"

# Rare random walk output
PATH_OUTPUT_FOLDER_RW = os.path.join(PATH_OUTPUT, "rarw")
os.makedirs(PATH_OUTPUT_FOLDER_RW, exist_ok=True)

# Compare results
PATH_OUTPUT_COMPARE_RSLT = os.path.join(PATH_OUTPUT, f"compare_rank_{CONFIG}")
os.makedirs(PATH_OUTPUT_COMPARE_RSLT, exist_ok=True)
PATH_OUTPUT_COMPARE_RSLT_PER_PATIENT = os.path.join(PATH_OUTPUT_COMPARE_RSLT, "metric_patient")
os.makedirs(PATH_OUTPUT_COMPARE_RSLT_PER_PATIENT, exist_ok=True)

PATH_OUTPUT_DF_COMPARE_RANK_DIRECT = f"{PATH_OUTPUT_COMPARE_RSLT}/compare_rank_method.xlsx"

PATH_OUTPUT_COMPARE_RSLT_ANALYSIS_PER_PATIENT = os.path.join(PATH_OUTPUT_COMPARE_RSLT, "analysis_per_patient")
os.makedirs(PATH_OUTPUT_COMPARE_RSLT_ANALYSIS_PER_PATIENT, exist_ok=True)
PATH_OUTPUT_COMPARE_METRIC_CLASSIF = os.path.join(PATH_OUTPUT_COMPARE_RSLT, "metric_classif")
os.makedirs(PATH_OUTPUT_COMPARE_METRIC_CLASSIF, exist_ok=True)
PATH_OUTPUT_COMPARE_GLOBAL = os.path.join(PATH_OUTPUT_COMPARE_RSLT, "global")
os.makedirs(PATH_OUTPUT_COMPARE_GLOBAL, exist_ok=True)

# Output product
PATH_OUTPUT_PRODUCT = os.path.join(PATH_OUTPUT, "pd_orphanet")
os.makedirs(PATH_OUTPUT_PRODUCT, exist_ok=True)
PATH_OUTPUT_PRODUCT_CLASSIF = os.path.join(PATH_OUTPUT_PRODUCT, "Classifications")
os.makedirs(PATH_OUTPUT_PRODUCT_CLASSIF, exist_ok=True)


PATH_OUTPUT_DF_PC_CLASSIF =f"{PATH_OUTPUT_PRODUCT}/parent_child_classif.xlsx"
PATH_OUTPUT_DF_PC =f"{PATH_OUTPUT_PRODUCT}/parent_child_noclassif.xlsx"
PATH_OUTPUT_DF_PC_CLASSIF_v2 =f"{PATH_OUTPUT_PRODUCT}/parent_child_classif_v2.xlsx"
PATH_OUTPUT_DF_PC_v2 =f"{PATH_OUTPUT_PRODUCT}/parent_child_noclassif_v2.xlsx"


PATH_OUTPUT_PRODUCT4_JSON_RSD =f"{PATH_OUTPUT_PRODUCT}/all_rsdpd4_mai_2025.json"
PATH_OUTPUT_DF_PRODUCT4_RSD =f"{PATH_OUTPUT_PRODUCT}/all_rsdpd4_mai_2025.xlsx"
PATH_OUTPUT_PRODUCT4_JSON =f"{PATH_OUTPUT_PRODUCT}/all_enpd_mai_2025.json"
PATH_OUTPUT_DF_PRODUCT4 =f"{PATH_OUTPUT_PRODUCT}/all_enpd_mai_2025.xlsx"
PATH_OUTPUT_DF_PRODUCT4_MATCH_RSD =f"{PATH_OUTPUT_PRODUCT}/all_enpd_mai_2025_same_rd_rsd_v2.xlsx"


COL_DF_PRODUCT4_ORPHACODE = 'ORPHAcode'

PATH_LIST_PRODUCT4 =f"{PATH_OUTPUT_PRODUCT}/list_rds.txt"
PATH_YAML_PRODUCT4 =f"{PATH_OUTPUT_PRODUCT}/RDs_all.yaml"
PATH_CLASSIFICATION_JSON =f"{PATH_OUTPUT_PRODUCT}/classif_orpha.json"


PATH_OUTPUT_PRODUCT7_JSON =f"{PATH_OUTPUT_PRODUCT}/en_product7.json"
PATH_OUTPUT_DF_PRODUCT7 =f"{PATH_OUTPUT_PRODUCT}/en_product7.xlsx"
PATH_OUTPUT_PRODUCT1_JSON =f"{PATH_OUTPUT_PRODUCT}/en_product1.json"
PATH_OUTPUT_DF_PRODUCT1 =f"{PATH_OUTPUT_PRODUCT}/en_product1.xlsx"

# Input product
PATH_INPUT_PRODUCT = os.path.join(PATH_INPUT, "pd_orphanet")
os.makedirs(PATH_INPUT_PRODUCT, exist_ok=True)

PATH_INPUT_PRODUCT4RSD_XML =f"{PATH_INPUT_PRODUCT}/all_rsdpd4_mai_2025.xml"
PATH_INPUT_PRODUCT4_XML =f"{PATH_INPUT_PRODUCT}/all_enpd_mai_2025.xml"
PATH_INPUT_PRODUCT1_XML =f"{PATH_INPUT_PRODUCT}/en_product1.xml"
PATH_INPUT_PRODUCT7_XML =f"{PATH_INPUT_PRODUCT}/en_product7.xml"

PATH_INPUT_PRODUCTCLASSIF_XML = os.path.join(PATH_INPUT_PRODUCT, "Classifications")
os.makedirs(PATH_INPUT_PRODUCTCLASSIF_XML, exist_ok=True)
PATH_INPUT_PREVALENCE =f"{PATH_INPUT_PRODUCT}/prevalences.json"


PATH_INPUT_PATIENTS_FOLDER = os.path.join(PATH_INPUT, "patient", "SolveRD_WP1_phenopackets_v2_with_ern_13301")
os.makedirs(PATH_INPUT_PATIENTS_FOLDER, exist_ok=True)
PATH_INPUT_PATIENTS_FOLDER_ONTOLOGYX = os.path.join(PATH_INPUT, "patient", "study_population")
os.makedirs(PATH_INPUT_PATIENTS_FOLDER_ONTOLOGYX, exist_ok=True)

PATH_INPUT_PATIENTS_FC =f"{PATH_INPUT}/patient/PATIENTS_SOLVED_FC_v2.xlsx"
PATH_INPUT_STEP_A2 =f"{PATH_INPUT}/stepA2.tsv"
###############################################################################
import os 
import time
import sys

import json 


from pyhpo import Ontology,HPOSet
Ontology(PATH_INPUT_HPO,transitive=True)
print(Ontology.version())



import pandas as pd
import numpy as np

import yaml

import logging

import glob

import argparse
 
import networkx as nx
import matplotlib.pyplot as plt
 
import seaborn as sns

import logging

from difflib import SequenceMatcher # for compare rank factors 2

import argparse

from scipy.stats import hmean

##############################################################################################################################################################











 
print(f"\n\n############################################")
print(f"\n\n############################################")

print(f"START  13_harmonic_mean_df")
print(f"START  13_harmonic_mean_df")

t0 = time.perf_counter()
# #############################################
# ## Set up argument parsing
# parser = argparse.ArgumentParser(description="Process inputs for the script.")

# # Arguments for file paths and file names
# parser.add_argument('--alpha', type=str, required=True)

# # Parse the arguments
# args = parser.parse_args()
 
# alpha = args.alpha

# #############################################

df_global_classif = pd.read_excel(PATH_OUTPUT_COMPARE_GLOBAL + "/global_classif.xlsx",index_col=0)

df_f =  df_global_classif[["type","method","group_id","rd_id","rank","is_rdi"]]
df_f = df_f.drop_duplicates()
list_patient = df_f['type'].unique()
list_method = df_f['method'].unique()



all_interaction = []
for onep in list_patient:
    mini_df = df_f[df_f['type'] == onep]
    # get the RDI
    rdi_ids = mini_df.loc[mini_df["is_rdi"] == "y", "rd_id"].unique()

    # make the calculation for each methods
    for onem in list_method:
        mini_mini_df = mini_df[mini_df['method'] == onem]
        # get the RDI group 
        list_rdi_groups = mini_mini_df[mini_mini_df["rd_id"].isin(rdi_ids)]['group_id'].unique()
        # get the RD with the same group as rdi (including the rdi )
        rd_match_group_rdi = mini_mini_df[mini_mini_df['group_id'].isin(list_rdi_groups)]['rd_id'].unique()

        # get the df 
        ## rd_match_group_rdi ici c'est les RDs qui ont un groupe similaire mais il peuvent avoir d'autre groupe qui ,e match pas le group rdi d'ou la seconde filtration on ne garde que les ranks des RD qui matche le groupe (normalement ca change rien mais c'est plus propre)
        df_match_group_rdi = mini_mini_df[(mini_mini_df['rd_id'].isin(rd_match_group_rdi)) & mini_mini_df['group_id'].isin(list_rdi_groups)].drop_duplicates()
        # df_match_group_rdi_without_rdi = df_match_group_rdi[df_match_group_rdi['is_rdi'] == "n"]

        # get the rank of each RDs in df format
        df_for_hm = df_match_group_rdi[['rd_id','rank']].drop_duplicates()

        ## for rank rdi 
        df_match_group_rdi_only_rdi = df_match_group_rdi[df_match_group_rdi['is_rdi'] == "y"]
        df_for_hm_rdi = df_match_group_rdi_only_rdi[['rd_id','rank']].drop_duplicates()

        # # extract ranks
        ranks_gp = df_for_hm['rank']
        ranks_rdi = df_for_hm_rdi['rank'].values[0]
        
        print(f"{onep} - {onem}\t RDI : {rdi_ids} rank {ranks_rdi}")
        print(f"{onep} - {onem}\t RDs match group RDI  - Nb  {len(ranks_gp)} ")

        # calculate the harmonic rank 
        try:
            # hm
            h_mean_rd_same_group_rdi = len(ranks_gp) / sum(1.0 / r for r in ranks_gp)

            print(f"{onep} - {onem}\tHarmonic mean (manual calculation) for rd same group RDI: {h_mean_rd_same_group_rdi}")
        except ZeroDivisionError:
            h_mean_rd_same_group_rdi = 0
            # h_mean_rd_same_group_no_rdi = 0
            print(f"{onep} - {onem}\t ZeroDivisionError")

        #for oner in ranks_gp:
        all_interaction.append((onep,onem,h_mean_rd_same_group_rdi,ranks_rdi)) #h_mean_rd_same_group_no_rdi ranks_rdi

df_hm_general_nof = pd.DataFrame(all_interaction,columns=['patient','method','hm_rd_same_groupe','rank_rdi']) #'hm_group_without_rdi'])
patient_before = df_hm_general_nof["patient"]
df_hm_general = df_hm_general_nof.dropna()
patient_after = df_hm_general["patient"].drop_duplicates()
lack_patient = set(patient_before).difference(patient_after)

print(f" {len(lack_patient)} don't have RDI in the pd4 -> REMOVED ")

# df_hm_general.to_excel('hm_general.xlsx')

df_hm_rdi  = df_hm_general[['patient','method','rank_rdi']].drop_duplicates()
df_hm_group  = df_hm_general[['patient','method','hm_rd_same_groupe']]
# df_hm_group_no_rdi  = df_hm_general[['patient','method','hm_group_without_rdi']]





 

# Compute the average HM for each method
mean_hm_group = (
    df_hm_group
    .groupby('method', as_index=False)['hm_rd_same_groupe']
    .mean()
    .rename(columns={'hm_rd_same_groupe': 'mean_hm_rd_same_groupe'})
)

# 2. Harmonic mean of hm_rd_same_groupe
harmonic_hm_group = (
    df_hm_group
    .groupby('method', as_index=False)['hm_rd_same_groupe']
    .agg(hm_hm_rd_same_groupe=hmean)
)

# 3. Harmonic mean of rank_rdi
harmonic_rank = (
    df_hm_rdi
    .groupby('method', as_index=False)['rank_rdi']
    .agg(hm_rank_rdi=hmean)
)

# Merge all into one DataFrame
summary_df = mean_hm_group.merge(harmonic_hm_group, on='method').merge(harmonic_rank, on='method')


# method_hm_group.to_excel(PATH_OUTPUT_COMPARE_RSLT + "hm_group_rarw_" + str(alpha)+ ".xlsx")



################################################
df_compare = pd.read_excel(PATH_OUTPUT_COMPARE_RSLT + "/" + "compare_rank_method.xlsx",index_col=0)
df_compare = df_compare.dropna()
all_interecation = []
rank_method = df_compare['RSD'].astype(float)
harmonic_mean = len(rank_method) / (1.0 / rank_method).sum()
all_interecation.append(('RSD',harmonic_mean))
rank_method = df_compare['RA'].astype(float)
harmonic_mean = len(rank_method) / (1.0 / rank_method).sum()
all_interecation.append(('RA',harmonic_mean))
rank_method = df_compare['RARW'].astype(float)
harmonic_mean = len(rank_method) / (1.0 / rank_method).sum()
all_interecation.append(('RARW',harmonic_mean))

df_hm_general_2 = pd.DataFrame(all_interecation,columns=['method','CR_hm_rank_rdi'])  



summary_df = summary_df.merge(df_hm_general_2, on='method', how='left')
 

print(f"END  13_harmonic_mean_df done in {time.perf_counter() - t0:.1f}s")
print(f"END  13_harmonic_mean_df done in {time.perf_counter() - t0:.1f}s")



 