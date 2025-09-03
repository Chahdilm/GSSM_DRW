from bin.set_log import *
from bin.path_variable import (
    PATH_OUTPUT_FOLDER_MATRIX_ADD_PATIENT, 
    PATH_OUTPUT_DF_PATIENT_ONLY_DISORDER,
    PATH_OUTPUT_SM,
    PATH_OUTPUT_MM,
    COL_DF_PATIENT_PATIENT,
    )


# Ensure base output directory exists
output_dir = PATH_OUTPUT_FOLDER_MATRIX_ADD_PATIENT
noslash = output_dir.rstrip('/')
os.makedirs(noslash, exist_ok=True)

#####################################################################################""
## Parse command-line arguments
parser = argparse.ArgumentParser(
    description="Add patient(s) into an existing MM matrix"
)
parser.add_argument(
    "--mm_prefix",
    required=True,
    help="Filename of the base MM matrix (e.g. mm_from_pd4_april2025.xlsx)",
)
parser.add_argument(
    "--sm_prefix",
    required=True,
    help="Prefix of the similarity-measure files (e.g. resnik_y_en_product4_avril2025_)",
)
args = parser.parse_args()

mm_prefix        = args.mm_prefix
sm_prefix        = args.sm_prefix.rstrip('_')
#####################################################################################""

# mm_prefix="1_1_1_1_1_concat_matrix"
# sm_prefix='3_2_2_2_1_rsd_resnik_n_productmai2024_all_vectors_withontologyX' #"resnik_y_en_product4_avril2025_"
 
#####################################################################################""
mm_file= f"{mm_prefix}.xlsx"
sm_file= f"{sm_prefix}.xlsx"



os.makedirs(PATH_OUTPUT_FOLDER_MATRIX_ADD_PATIENT, exist_ok=True)
# Create subdir for this SM run
run_dir = os.path.join(
    PATH_OUTPUT_FOLDER_MATRIX_ADD_PATIENT,
    mm_prefix
)
os.makedirs(run_dir, exist_ok=True)

print("2.START add patient to the matrix:")
# Load base matrix
df_matrice = pd.read_excel(
    os.path.join(PATH_OUTPUT_MM, mm_file),
    index_col=0
)

# df_matrice_m = df_matrice.pivot(index='OC1', columns='OC2', values='score')
# df_matrice_m.to_excel(f"{PATH_OUTPUT_MM}/matrix_{mm_file}")
print('Base matrix imported')
 
# Load patient list
df_patient = pd.read_excel(PATH_OUTPUT_DF_PATIENT_ONLY_DISORDER, index_col=0)
# df_patient = df_patient[df_patient[COL_DF_PATIENT_PATIENT] == "P0001068"]
print('Patient df imported')
user_seed = df_patient[COL_DF_PATIENT_PATIENT].drop_duplicates().tolist()
print(f'{len(user_seed)} patients to integrate')

# Load similarity scores
df_sm = pd.read_excel(
    os.path.join(PATH_OUTPUT_SM, sm_file),
    index_col=0
)
 
df_sm_d = df_sm.drop_duplicates(subset=['patients', 'RDs'])
print('Similarity DF imported')
# check the duplicated 
# duplicates = df_sm[df_sm.duplicated(subset=['patients', 'RDs'], keep=False)]
# print(duplicates)
sm_pivot =  df_sm_d.pivot(index='patients', columns='RDs', values='score')

i=0

 

# Iterate and add each patient
for patient in user_seed:
    out_csv = os.path.join(run_dir, f"{patient}.csv")

    if patient in out_csv:
        print(patient,i)
        t0 = time.perf_counter()
    
        scores = sm_pivot.loc[patient]
        # Defragment DataFrame storage for next iteration
        df_matrice_perp= df_matrice.copy()

        # Add column and row
        df_matrice_perp[patient] = scores.reindex(df_matrice_perp.index).fillna(0)
        df_matrice_perp.loc[patient] = scores.reindex(df_matrice_perp.columns).fillna(0)
        df_matrice_perp.at[patient, patient] = 0

        # Save per-patient version
        df_matrice_perp.to_csv(out_csv)
        print(f"Inserted {patient}; saved in {time.perf_counter() - t0:.1f}s")
        i=i+1
    else:
        print("patient already integrated ")

################## 
# ## Add gene  -> i prefer to add it in the script 4_rarw.py
# ##################
# match_gene = {}
# path_patient = "/home/maroua/Bureau/my_pipeline_v3/GSSM_DRW/input/patient/SolveRD_WP1_phenopackets_v2_with_ern_13301/"

# for patient in user_seed:
#     ## get the gene from the json file 
#     with open(f"{path_patient}/{patient}_ern.json", 'r', encoding="ISO-8859-1" ) as f:
#         root_json = json.load(f)
#         interp = root_json['interpretations']
#         for onedict in interp:
#             diag = onedict['diagnosis']['genomicInterpretations']
#             for one_diag in diag:
#                 if 'variantInterpretation' in one_diag:
#                     gene_patient = one_diag['variantInterpretation']['variationDescriptor']['geneContext']['symbol']
#                     interactions.add((patient,gene_patient))
#                 elif 'gene' in one_diag:
#                     gene_patient = one_diag['gene']['symbol']
#                     interactions.add((patient,gene_patient))


# interactions = set()
# df_pd6 = pd.read_excel("/home/maroua/Bureau/my_pipeline_v3/GSSM_DRW/output/pd_orphanet/en_product6.xlsx",index_col=0 )
# rd_list = list(df_matrice.columns)
# for onerd in rd_list:
#     try:
#         get_gene_rd = df_pd6[df_pd6['ORPHACode'] == onerd]['Symbol'].tolist()
#     except:
#         get_gene_rd = np.nan

#     for onele in get_gene_rd:
#         interactions.add((onerd,onele))
# df_gene_inter = pd.DataFrame(list(interactions), columns=['entity','gene'])



 
 
# # Collect unique genes
# genes = sorted(df_gene_inter["gene"].unique().tolist())

# # Build augmented index/columns = entities + genes
# new_index = list(df_matrice_perp.index) + genes
# new_cols = list(df_matrice_perp.columns) + genes

# # Start with all zeros
# df_matrice_patient_gene = pd.DataFrame(0.0, index=new_index, columns=new_cols)

# # Put back the original matrix values
# df_matrice_patient_gene.loc[df_matrice_perp.index, df_matrice_perp.columns] = df_matrice_perp.values

# # Fill entity–gene and gene–entity with 1 when mapping exists
# for ent, g in df_gene_inter.itertuples(index=False):
#     df_matrice_patient_gene.at[ent, g] = 1.0   # entity -> gene
#     df_matrice_patient_gene.at[g, ent] = 1.0   # gene -> entity (symmetric)


# out_xlsx = os.path.join(run_dir, f"{patient}_gene_intersection.xlsx")
# df_gene_inter.to_excel(out_xlsx)