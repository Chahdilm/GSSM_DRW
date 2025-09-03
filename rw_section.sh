
#!/usr/bin/env bash
set -euo pipefail

cd bin/

 
# this block will print one patient ID per line
mapfile -t PATIENTS < <(python3 - <<EOF
import pandas as pd
from path_variable import PATH_OUTPUT_DF_PATIENT_ONLY_DISORDER, COL_DF_PATIENT_PATIENT

df = pd.read_excel(PATH_OUTPUT_DF_PATIENT_ONLY_DISORDER, index_col=0)
#df = df[df['phenopacket'] == "P0007806" ]
for p in df[COL_DF_PATIENT_PATIENT].drop_duplicates():
    print(p)
EOF
)
# # remove the first element
# PATIENTS=( "${PATIENTS[@]:1}" )
# echo $PATIENTS


ALPHA_STRINGS=(
  # 1.0
  # 0.9
  # 0.8
  # 0.5
 # 0.1
  # 0.05
  # 0.01
  0.3
  #  0.25
  #  0.2
  #  0.15
  # 0.5
  # 0.05
  #0.4
  # 0.35
  #0.45
  #0.6
  # 0.7
)
 
 
mm_type="mm_1_1_1_1_1" #'mm_1_1_1_1_1' #mm_3_2_2_2_1
mp_type="mp_3_2_2_2_1"  # 'mp_1_1_1_1_1' # 'mp_3_2_2_2_1'

#  loop over each alpha value 
for user_alpha in "${ALPHA_STRINGS[@]}"; do
  echo
  echo "######################################"
  echo "## Starting full run for α=$user_alpha"

  # parallel per-patient random‐walks
  parallel -j2 --halt soon,fail=1 \
    --joblog "log_parallel_alpha_${user_alpha}.txt" \
    --bar "
      echo '--- seed: {} (α=${user_alpha})' &&
      python3 4_rarw_gene.py \
        --alpha ${user_alpha} \
        --mm_type ${mm_type} \
        --mp_type ${mp_type} \
        --seed {}
    " ::: "${PATIENTS[@]}"




  # combine all patients into global matrix for this alpha
  python3 4_global_rarw.py \
    --matrix_subdir "${mm_type}"_"${mp_type}" \
    --alpha "$user_alpha"

  echo "Completed global run for α=$user_alpha"
done

echo " All patients are integrated in matrix mm (one by once) + rw complete ! "


################################################################################################################
 
mm_type="mm_1_1_1_1_1" #'mm_1_1_1_1_1' #mm_3_2_2_2_1
mp_type="mp_1_1_1_1_1"  # 'mp_1_1_1_1_1' # 'mp_3_2_2_2_1'

#  loop over each alpha value 
for user_alpha in "${ALPHA_STRINGS[@]}"; do
  echo
  echo "######################################"
  echo "## Starting full run for α=$user_alpha"

  # parallel per-patient random‐walks
  parallel -j2 --halt soon,fail=1 \
    --joblog "log_parallel_alpha_${user_alpha}.txt" \
    --bar "
      echo '--- seed: {} (α=${user_alpha})' &&
      python3 4_rarw_gene.py \
        --alpha ${user_alpha} \
        --mm_type ${mm_type} \
        --mp_type ${mp_type} \
        --seed {}
    " ::: "${PATIENTS[@]}"




  # combine all patients into global matrix for this alpha
  python3 4_global_rarw.py \
    --matrix_subdir "${mm_type}"_"${mp_type}" \
    --alpha "$user_alpha"

  echo "Completed global run for α=$user_alpha"
done

echo " All patients are integrated in matrix mm (one by once) + rw complete ! "



################################################################################################################
 
mm_type="mm_3_2_2_2_1" #'mm_1_1_1_1_1' #mm_3_2_2_2_1
mp_type="mp_1_1_1_1_1"  # 'mp_1_1_1_1_1' # 'mp_3_2_2_2_1'

#  loop over each alpha value 
for user_alpha in "${ALPHA_STRINGS[@]}"; do
  echo
  echo "######################################"
  echo "## Starting full run for α=$user_alpha"

  # parallel per-patient random‐walks
  parallel -j2 --halt soon,fail=1 \
    --joblog "log_parallel_alpha_${user_alpha}.txt" \
    --bar "
      echo '--- seed: {} (α=${user_alpha})' &&
      python3 4_rarw_gene.py \
        --alpha ${user_alpha} \
        --mm_type ${mm_type} \
        --mp_type ${mp_type} \
        --seed {}
    " ::: "${PATIENTS[@]}"




  # combine all patients into global matrix for this alpha
  python3 4_global_rarw.py \
    --matrix_subdir "${mm_type}"_"${mp_type}" \
    --alpha "$user_alpha"

  echo "Completed global run for α=$user_alpha"
done

echo " All patients are integrated in matrix mm (one by once) + rw complete ! "



################################################################################################################
 
mm_type="mm_3_2_2_2_1" #'mm_1_1_1_1_1' #mm_3_2_2_2_1
mp_type="mp_3_2_2_2_1"  # 'mp_1_1_1_1_1' # 'mp_3_2_2_2_1'

#  loop over each alpha value 
for user_alpha in "${ALPHA_STRINGS[@]}"; do
  echo
  echo "######################################"
  echo "## Starting full run for α=$user_alpha"

  # parallel per-patient random‐walks
  parallel -j2 --halt soon,fail=1 \
    --joblog "log_parallel_alpha_${user_alpha}.txt" \
    --bar "
      echo '--- seed: {} (α=${user_alpha})' &&
      python3 4_rarw_gene.py \
        --alpha ${user_alpha} \
        --mm_type ${mm_type} \
        --mp_type ${mp_type} \
        --seed {}
    " ::: "${PATIENTS[@]}"




  # combine all patients into global matrix for this alpha
  python3 4_global_rarw.py \
    --matrix_subdir "${mm_type}"_"${mp_type}" \
    --alpha "$user_alpha"

  echo "Completed global run for α=$user_alpha"
done

echo " All patients are integrated in matrix mm (one by once) + rw complete ! "
