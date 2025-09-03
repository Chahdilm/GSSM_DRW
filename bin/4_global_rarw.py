
import os
import pandas as pd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--matrix_subdir",required=True)
parser.add_argument("--alpha",required=True)

args = parser.parse_args()
matrix_subdir = args.matrix_subdir
alpha = str(args.alpha)

# matrix_subdir='mm_1_1_1_1_1_mp_1_1_1_1_1'
# alpha=str(0.30)
PATH_OUTPUT_FOLDER_RW = "/home/maroua/Bureau/my_pipeline_v3/GSSM_DRW/output/rarw/"

# Directory where per-patient rarw are stored
rarw_dir = os.path.join(
        PATH_OUTPUT_FOLDER_RW,
        alpha,
        matrix_subdir
    )
xlsx_files = os.listdir(rarw_dir) 

PATH_OUTPUT_DF_PATIENT_ONLY_DISORDER = "/home/maroua/Bureau/my_pipeline_v3/GSSM_DRW/output/patient_solverd/patient_confirmed_solverd_only_disorder_with_ontologyX.xlsx"
COL_DF_PATIENT_PATIENT = "phenopacket"
# Load patient list
df_patient = pd.read_excel(PATH_OUTPUT_DF_PATIENT_ONLY_DISORDER, index_col=0)
print('Patient df imported')
user_seed = df_patient[COL_DF_PATIENT_PATIENT].drop_duplicates().tolist()
print(f'{len(user_seed)} patients to integrate')

all_interaction = set()
for patient in xlsx_files:
    try:
        patient_from_df_patients= df_patient[df_patient['phenopacket'] == patient.replace("_gene.xlsx",'')]
        rdi = patient_from_df_patients['Disease'].values[0]
        df_rarw= pd.read_excel(f"{PATH_OUTPUT_FOLDER_RW}/{alpha}/{matrix_subdir}/{patient}")
        df_rarw.rename(columns={'Unnamed: 0':'RD'}, inplace=True)
        rank_pg = df_rarw[df_rarw['RD'] == rdi]
        all_interaction.add((patient.replace(".xlsx",''),rdi,rank_pg['pg'].values[0],int(rank_pg['rank_pg'].values[0])))
    except IndexError:
        print(f'{patient} no rdi maybe error')

df_f = pd.DataFrame(all_interaction,columns=['patients','RDs','score','rank'])
output_path = os.path.join(PATH_OUTPUT_FOLDER_RW,alpha, f"RARW_{matrix_subdir}.xlsx")
df_f.to_excel(output_path)