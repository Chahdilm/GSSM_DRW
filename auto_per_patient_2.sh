#!/usr/bin/env bash
set -euo pipefail


#############################################
### Define variables
#############################################
user_nb_top_rd=50

# List of α values to try
ALPHA_STRINGS=(
  0.1
  0.01  
  0.2 
  0.3
  0.4
  0.5 
  0.05  
  0.8
  0.9
  0.15  
  0.25 
  0.35
  0.45
  1.0
  0.6
  0.7
)
# this block will print one patient ID per line
mapfile -t PATIENTS < <(python3 - <<EOF
import pandas as pd
from bin.set_log import PATH_OUTPUT_DF_PATIENT, COL_DF_PATIENT_PATIENT

df = pd.read_excel(PATH_OUTPUT_DF_PATIENT, index_col=0)
#df = df[df['phenopacket'] == "P0001068" ]
for p in df[COL_DF_PATIENT_PATIENT].drop_duplicates():
    print(p)
EOF
)
# remove the first element
PATIENTS=( "${PATIENTS[@]:1}" )
#echo "Found ${#PATIENTS[@]} patients:"
#printf '=> %s\n' "${PATIENTS[@]}"


config_vect='1_1_1_1_1_concat_matrix'
ra='3_2_2_2_1_rsd_resnik_n_productmai2024_all_vectors_withontologyX'
rarw='RARW_1_1_1_1_1_concat_matrix'

MAX_PAR=10          # Number of patients to run simultaneously


for user_alpha in "${ALPHA_STRINGS[@]}"; do
  echo
  echo "#############################################"
  echo "###   Starting full comparison for α=$user_alpha"
  echo "#############################################"

  # -- 1) configure
  cd bin || exit 1
  python3 config_rd.py \
    --config_rd "$config_vect" \
    --alpha "$user_alpha"
  cd ..

  python3 -m bin.compare_rslt.1_compare_rank_global --ra "$ra" --rarw "$rarw"  --alpha "$user_alpha"

  # -- 2) profile & stats (global, not α-specific)
  python3 -m bin.compare_rslt.3_profile_rdi_stat
  python3 -m bin.compare_rslt.3_profile_rd_patient_stat

  python3 -m bin.compare_rslt.4_metric_ranking_per_patient --ra "$ra" --alpha "$user_alpha"



# #   # -- 3) per-patient classification metrics
# #   for seed in "${PATIENTS[@]}"; do
# #     echo "--- seed: $seed (α=$user_alpha)"
# #     python3 -m bin.compare_rslt.5_metric_classif_per_patient \
# #       --user_nb_top_rd "$user_nb_top_rd" \
# #       --onep "$seed"
# #   done
    export user_nb_top_rd  # Make sure variables are visible to subprocesses
    export user_alpha
    parallel -j 20 --halt soon,fail=1 --joblog "log_parallel_alpha_${user_alpha}.txt" --bar '
    echo "--- seed: {} (α=$user_alpha)"
    python3 -m bin.compare_rslt.5_metric_classif_per_patient \
        --user_nb_top_rd "$user_nb_top_rd" \
        --onep {}
    ' ::: "${PATIENTS[@]}"
    

 
#   # -- 4) aggregate & final metrics (some take α into account)
#   python3 -m bin.compare_rslt.6_make_it_global
#   python3 -m bin.compare_rslt.8_cdf_auc_v2
  python3 -m bin.compare_rslt.13_harmonic_mean_df --alpha "$user_alpha"
  # python3 -m bin.compare_rslt.12_get_match_group

  echo " Completed all steps for α=$user_alpha"
done


echo " All α values processed!"
 
# ##################################################################
# set -euo pipefail


# #############################################
# ### Define variables
# #############################################
# user_nb_top_rd=50


# # default list, if no args given
 


# # this block will print one patient ID per line
# mapfile -t PATIENTS < <(python3 - <<EOF
# import pandas as pd
# from bin.set_log import PATH_OUTPUT_DF_PATIENT, COL_DF_PATIENT_PATIENT

# df = pd.read_excel(PATH_OUTPUT_DF_PATIENT, index_col=0)
# #df = df[df['phenopacket'] == "P0001068" ]
# for p in df[COL_DF_PATIENT_PATIENT].drop_duplicates():
#     print(p)
# EOF
# )
# # remove the first element
# PATIENTS=( "${PATIENTS[@]:1}" )
# #echo "Found ${#PATIENTS[@]} patients:"
# #printf '=> %s\n' "${PATIENTS[@]}"


# config_vect='1_1_1_1_1_concat_matrix'
# ra='3_2_2_2_1_rsd_resnik_n_productmai2024_all_vectors_withontologyX'
# rarw='RARW_1_1_1_1_1_concat_matrix'
# alpha=0.30

# cd bin || exit 1

# python3 config_rd.py --config_rd "$config_vect"  --alpha "$alpha"
# cd ..
# # python3 -m bin.compare_rslt.1_compare_rank_global --ra "$ra" --rarw "$rarw"  --alpha "$alpha"

# # python3 -m bin.compare_rslt.2_rank_global
# # cp output/mp_sm/compare_rank_$config_rd.xlsx output/compare_rank_$config_rd/compare_rank_$config_rd.xlsx 
# ## the script 3 is the same qu'importe les donnée de ranking car on  regarde maladie et patient (a mettre autre part)
# python3 -m bin.compare_rslt.3_profile_rdi_stat
# # python3 -m bin.compare_rslt.4_metric_ranking_per_patient --ra "$ra" --alpha "$alpha"

# python3 -m bin.compare_rslt.3_profile_rd_patient_stat

# for seed in "${PATIENTS[@]}"; do
# echo "--- seed: $seed"
# python3 -m bin.compare_rslt.5_metric_classif_per_patient \
#     --user_nb_top_rd "$user_nb_top_rd" --onep "$seed"
# done
# python3 -m bin.compare_rslt.6_make_it_global
# python3 -m bin.compare_rslt.8_cdf_auc_v2
# python3 -m bin.compare_rslt.13_harmonic_mean_df --alpha "$alpha"

# python3 -m bin.compare_rslt.12_get_match_group
