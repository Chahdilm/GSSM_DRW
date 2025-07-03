#!/usr/bin/env bash
set -euo pipefail
VECTOR_STRINGS='3_2_2_2_1'
 


## name of the file where the matrix was build 
# funsimmax_resnik_n_productmai2024_with_rsdinRA_ontologyX_1_1_1_1_0
mm_prefix="3_2_2_2_1_concat_matrix"
sm_prefix='_rsd_resnik_n_productmai2024_all_vectors_withontologyX' #"resnik_y_en_product4_avril2025_"

method='resnik'
combine='funSimMax'

# echo "======================================"
# echo "  Build matrix MM($VECTOR_STRINGS)"
# echo "======================================"
# python3 -m bin.3_build_mm --name_matrix "$mm_prefix" --combine "$combine" --method "$method" --vector_str "$VECTOR_STRINGS"


echo
echo "======================================"
echo "  Integrate patients into MM ($VECTOR_STRINGS)"
echo "======================================"
python -m bin.4_intagrate_patient_in_mm --mm_prefix "$mm_prefix" --sm_prefix "${VECTOR_STRINGS}${sm_prefix}"


 