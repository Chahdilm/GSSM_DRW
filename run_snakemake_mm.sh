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
pdtype_pattern='pd4_match_rsd_exeinsept2025' 

## for the integration part :
sm_prefix='3_2_2_2_1_rsd_resnik_n_productmai2024_all_vectors_withontologyX'
#'3_2_2_2_1_rsd_resnik_n_productmai2024_all_vectors_withontologyX' #"resnik_y_en_product4_avril2025_"
# 1_1_1_1_1_rsd_resnik_n_productmai2024_controvector_withontologyX

for VS in "${VECTOR_STRINGS[@]}"; do
  echo "======================================"
  echo "  Snakemake: vector_str = $VS"
  echo "======================================"

  PYTHONPATH=$(pwd) snakemake \
    --snakefile bin/Snakefile.projetmm \
    --cores 22 \
    --config vector_str="$VS"
  ## snakemake --snakefile bin/Snakefile.projetmm --cores 22 --config vector_str="$VS"
  ## snakemake --cores 22 --config vector_str=1_0_0_0


  echo "======================================"
  echo "  concat_matrix vector_str = $VS"
  echo "======================================"

  python3 -m bin.2_concat_both concat_matrix \
      -v "$VS" \
    --col1 "$name_col1" \
    --col2 "$name_col2" \
    --pdtype_pattern "$pdtype_pattern"


 
  echo
  echo "======================================"
  echo "  Integrate patients into MM ($VS)"
  echo "======================================"
  python -m bin.3_intagrate_patient_in_mm --mm_prefix "${VS}" --sm_prefix "${sm_prefix}"


done

echo " All Snakemake runs + post-processing complete!"




