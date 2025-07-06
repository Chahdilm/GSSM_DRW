#!/usr/bin/env bash
set -euo pipefail


 

# which vectors to run
VECTOR_STRINGS=( 
  # '3_2_2_2_1'
  '1_1_1_1_1' 
  )

## for the concat part 
name_col1='OC1'
name_col2='OC2'
pdtype_pattern='productmai2024_all_vectors_withontologyX' 

## for the integration part :
mm_prefix="_concat_matrix"
sm_prefix='1_1_1_1_1_rsd_resnik_n_productmai2024_controvector_withontologyX'
#'3_2_2_2_1_rsd_resnik_n_productmai2024_all_vectors_withontologyX' #"resnik_y_en_product4_avril2025_"
 

for VS in "${VECTOR_STRINGS[@]}"; do
  echo "======================================"
  echo "  Snakemake: vector_str = $VS"
  echo "======================================"

  cd bin/
  snakemake --snakefile Snakefile.projetmm --cores 22 --config vector_str="$VS"
  # # snakemake --cores 22 --config vector_str=1_0_0_0

  echo "======================================"
  echo "  concat_matrix vector_str = $VS"
  echo "======================================"

  python3 2_concat_both.py concat_matrix \
      -v "$VS" \
    --col1 "$name_col1" \
    --col2 "$name_col2" \
    --pdtype_pattern "$pdtype_pattern"


 
  echo
  echo "======================================"
  echo "  Integrate patients into MM ($VS)"
  echo "======================================"
  python -m 3_intagrate_patient_in_mm --mm_prefix "${VS}${mm_prefix}" --sm_prefix "${sm_prefix}"


done

echo " All Snakemake runs + post-processing complete!"



 
# #!/usr/bin/env bash
# set -euo pipefail

# VECTOR_STRINGS=( '1_1_1_1_1' )
# name_col1='OC1'
# name_col2='OC2'
# pdtype_pattern='productmai2024_all_vectors_withontologyX'

# mm_prefix="_concat_matrix"
# sm_prefix="1_1_1_1_1_rsd_resnik_n_productmai2024_controvector_withontologyX"
# # sm_prefix="3_2_2_2_1_rsd_resnik_n_${pdtype_pattern}"

# # draw a bar of width characters, filling 'filled' segments
# progress_bar() {
#   local filled=$1 total=$2 width=40
#   local pct=$(( 100 * filled / total ))
#   local fill_chars=$(( width * filled / total ))
#   local empty_chars=$(( width - fill_chars ))
#   printf "\r[%-${width}s] %3d%%" \
#          "$(printf '#%.0s' $(seq 1 $fill_chars))$(printf ' %.0s' $(seq 1 $empty_chars))" \
#          "$pct"
# }

# for VS in "${VECTOR_STRINGS[@]}"; do
#   echo
#   echo "======================================"
#   echo " vector_str = $VS"
#   echo "======================================"

#   total=3
#   step=1

#   # 1) Snakemake
#   printf "\nStep %d/%d: running Snakemake...\n" "$step" "$total"
#   cd bin/
#   snakemake --snakefile Snakefile.projetmm --cores 22 --config vector_str="$VS"
#   cd - >/dev/null
#   progress_bar $step $total
#   step=$((step+1))

#   cd bin/
#   2) concat_matrix
#   printf "\nStep %d/%d: post-processing concat_matrix...\n" "$step" "$total"
#   python3 2_concat_both.py concat_matrix \
#     -v "$VS" \
#     --col1 "$name_col1" \
#     --col2 "$name_col2" \
#     --pdtype_pattern "$pdtype_pattern"
#   progress_bar $step $total
#   step=$((step+1))

#   # 3) integrate patients
#   printf "\nStep %d/%d: integrating patients into MM...\n" "$step" "$total"
#   python3 4_intagrate_patient_in_mm.py \
#     --mm_prefix "${VS}${mm_prefix}" \
#     --sm_prefix "${sm_prefix}"
#   progress_bar $step $total

#   echo -e "\n\n✔ All steps completed for $VS!"
# done

