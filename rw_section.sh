
#!/usr/bin/env bash
set -euo pipefail

cd bin/

 
# this block will print one patient ID per line
mapfile -t PATIENTS < <(python3 - <<EOF
import pandas as pd
from path_variable import PATH_OUTPUT_DF_PATIENT_ONLY_DISORDER_WITH_ONTOLOGYX, COL_DF_PATIENT_PATIENT

df = pd.read_excel(PATH_OUTPUT_DF_PATIENT_ONLY_DISORDER_WITH_ONTOLOGYX, index_col=0)
df = df[df['phenopacket'] == "P0007806" ]
for p in df[COL_DF_PATIENT_PATIENT].drop_duplicates():
    print(p)
EOF
)
# # remove the first element
# PATIENTS=( "${PATIENTS[@]:1}" )
# echo $PATIENTS

# vector config for mm 
VECTOR_STRINGS='1_1_1_1_1' #'3_2_2_2_1'

## name of the mp best config 
sm_prefix='_concat_matrix' #"resnik_y_en_product4_avril2025_"
 


ALPHA_STRINGS=(
  # 1.0
  # 0.9
  # 0.8
  # 0.5
 # 0.1
  # 0.05
  # 0.01
  # # 0.3
  #  0.25
  #  0.2
  #  0.15
  # 0.5
  # 0.05
  #0.4
  # 0.35
  #0.45
  0.6
  # 0.7
)
 

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
    python3 4_rarw.py run --alpha ${user_alpha} \
          --matrix_subdir ${VECTOR_STRINGS}${sm_prefix} \
          --seeds {}
  " ::: "${PATIENTS[@]}"
 


  # combine all patients into global matrix for this alpha
  python3  4_rarw.py  aggregate \
    --matrix_subdir "${VECTOR_STRINGS}${sm_prefix}" \
    --alpha "$user_alpha"

  echo "Completed global run for α=$user_alpha"
done

echo " All patients are integrated in matrix mm (one by once) + rw complete ! "


################################################################################################################

# #!/usr/bin/env bash
# set -euo pipefail

# cd bin/

# # this block will print one patient ID per line
# mapfile -t PATIENTS < <(python3 - <<EOF
# import pandas as pd
# from path_variable import (
# PATH_OUTPUT_DF_PATIENT_ONLY_DISORDER_WITH_ONTOLOGYX,
# COL_DF_PATIENT_PATIENT,
#  )

# df = pd.read_excel(PATH_OUTPUT_DF_PATIENT_ONLY_DISORDER_WITH_ONTOLOGYX, index_col=0)
# df = df[df['phenopacket'] == "P0007806" ]
# for p in df[COL_DF_PATIENT_PATIENT].drop_duplicates():
#     print(p)
# EOF
# )
# # # remove the first element
# # PATIENTS=( "${PATIENTS[@]:1}" )
# # echo $PATIENTS

# # vector config for mm 
# VECTOR_STRINGS='1_1_1_1_1' #'3_2_2_2_1'

# ## name of the mp best config 
# sm_prefix='_concat_matrix' #"resnik_y_en_product4_avril2025_"
 


# ALPHA_STRINGS=(
#   # 1.0
#   # 0.9
#   # 0.8
#   # 0.5
#  # 0.1
#   # 0.05
#   # 0.01
#   # # 0.3
#   #  0.25
#   #  0.2
#   #  0.15
#   # 0.5
#   # 0.05
#   #0.4
#   # 0.35
#   #0.45
#   0.6
#   # 0.7
# )


# #  loop over each alpha value 
# for user_alpha in "${ALPHA_STRINGS[@]}"; do
#   echo
#   echo "######################################"
#   echo "## Starting full run for α=$user_alpha"

#   # parallel per-patient random‐walks
#   parallel -j2 --halt soon,fail=1 \
#           --joblog "log_parallel_alpha_${user_alpha}.txt" \
#           --bar "
#     echo '--- seed: {} (α=${user_alpha})' &&
#     python3 5_make_rarw.py --alpha ${user_alpha} \
#           --path_where_patientadded_is ${VECTOR_STRINGS}${sm_prefix} \
#           --seeds {}
#   " ::: "${PATIENTS[@]}"


#   # combine all patients into global matrix for this alpha
#   python3 6_global_rarw.py \
#     --matrix_subdir "${VECTOR_STRINGS}${sm_prefix}" \
#     --alpha "$user_alpha"

#   echo "Completed global run for α=$user_alpha"
# done

# echo " All patients are integrated in matrix mm (one by once) + rw complete ! "
