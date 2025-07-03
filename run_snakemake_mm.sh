#!/usr/bin/env bash
set -euo pipefail


 

# which vectors to run
VECTOR_STRINGS=( 
  # '3_2_2_2_1'
  '1_1_1_1_1' 
  )

name_col1='OC1'
name_col2='OC2'

## for the integration part :
mm_prefix="_concat_matrix"
sm_prefix='3_2_2_2_1_rsd_resnik_n_productmai2024_all_vectors_withontologyX' #"resnik_y_en_product4_avril2025_"
method='resnik'
combine='funSimMax'

for VS in "${VECTOR_STRINGS[@]}"; do
  echo "======================================"
  echo "  Snakemake: vector_str = $VS"
  echo "======================================"

  cd bin/
  snakemake --snakefile Snakefile.projetmm --cores 22 --config vector_str="$VS"
  # snakemake --cores 22 --config vector_str=1_0_0_0

  # echo "======================================"
  # echo " Post-processing Excel outputs for $VS"
  # python -m bin.2_concat_ra_mm --filter-type "$VS" --col1 "$name_col1" --col2 "$name_col2" 

 
  # echo
  # echo "======================================"
  # echo "  Integrate patients into MM ($VS)"
  # echo "======================================"
  # python -m bin.4_intagrate_patient_in_mm --mm_prefix "${VS}${mm_prefix}" --sm_prefix "${sm_prefix}"





done

echo " All Snakemake runs + post-processing complete!"
 



 

