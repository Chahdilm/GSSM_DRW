#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

pwd
#############################################
### Define variables
#############################################
user_nb_top_rd=50

# List of α values to try
ALPHA_STRINGS=(
0.01
0.05
0.1
0.15
0.2
0.25
0.3
0.35
0.4
0.45
0.5
0.6
0.7
0.8
0.9
1.0
)

# this block will print one patient ID per line
mapfile -t PATIENTS < <(python3 - <<EOF
import pandas as pd
from bin.path_variable import PATH_OUTPUT_DF_PATIENT_ONLY_DISORDER, COL_DF_PATIENT_PATIENT

df = pd.read_excel(PATH_OUTPUT_DF_PATIENT_ONLY_DISORDER, index_col=0)
#df = df[df['phenopacket'] == "d" ]
for p in df[COL_DF_PATIENT_PATIENT].drop_duplicates():
    print(p)
EOF
)
# remove the first element
# PATIENTS=( "${PATIENTS[@]:1}" )
echo "Found ${#PATIENTS[@]} patients:"
# printf '=> %s\n' "${PATIENTS[@]}"


config_vect='1_1_1_1_1_concat_matrix'
ra='3_2_2_2_1_rsd_resnik_n_productmai2024_all_vectors_withontologyX'
rarw='mm_1_1_1_1_1_mp_3_2_2_2_1'

MAX_PAR=10          # Number of patients to run simultaneously


for user_alpha in "${ALPHA_STRINGS[@]}"; do
  echo
  echo "#############################################"
  echo "###   Starting full comparison for α=$user_alpha"
  echo "#############################################"

  # -- 1) configure
 
  python3 bin/config_rd.py \
    --config_rd "$config_vect" \
    --alpha "$user_alpha"

 
  
  python3   -m bin.lauch_rslt.compare_rslt.1_compare_rank_global  --ra "$ra" --rarw "$rarw"  --alpha "$user_alpha"
  python3 -m bin.lauch_rslt.compare_rslt.4_metric_ranking_per_patient --ra "$ra" --alpha "$user_alpha"

 
  export user_nb_top_rd  # Make sure variables are visible to subprocesses
  export user_alpha
  parallel -j 20 --halt soon,fail=1 --joblog "log_parallel_alpha_${user_alpha}.txt" --bar '
  echo "--- seed: {} (α=$user_alpha)"
  python3 -m bin.lauch_rslt.compare_rslt.5_metric_classif_per_patient \
      --user_nb_top_rd "$user_nb_top_rd" \
      --onep {}
  ' ::: "${PATIENTS[@]}"
  


  # -- 4) aggregate & final metrics (some take α into account)
  python3 -m bin.lauch_rslt.compare_rslt.6_make_it_global
  python3 -m bin.lauch_rslt.compare_rslt.13_harmonic_mean  --topn 10  --hierarchy_level 5
  done


LEVEL_STRINGS=(
1
2
3
4
5

)

for level in "${LEVEL_STRINGS[@]}"; do

  for user_alpha in "${ALPHA_STRINGS[@]}"; do
    python3 bin/config_rd.py --config_rd "$config_vect" --alpha "$user_alpha"

    echo "###   Starting hm for level =$level  α=$user_alpha"  
    python3 -m bin.lauch_rslt.compare_rslt.13_harmonic_mean  --topn 15  --hierarchy_level "$level"

  done


done



# for level in "${LEVEL_STRINGS[@]}"; do

#   echo "Running script 14 for level $level"
#   python3 -m bin.lauch_rslt.compare_rslt.14_harmonic_mean_concat  --topn 15  --hierarchy_level "$level"
#   echo "Done with level $level"
# done
# echo " concat all hm rslt"

## ici faire une boucle de profondeur 


 
