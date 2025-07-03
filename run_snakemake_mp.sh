#!/usr/bin/env bash
set -euo pipefail


 

# which vectors to run
VECTOR_STRINGS=(
#  '1_1_0_1_0'
#  '0.99_0.77_0.65_0.63_0.94'
#  '2.74_5.21_9.96_12.36_3.07'
#  '0.98_0.18_0.01_0_0.77'
#  '0.01_0.60_0.92_1_0.15'
#  '5.16_0.90_0.46_0.39_2.54'
#  '5_3_2_1_4'
#  '5_2_1_1_3'
#  '1.2_0.9_0.7_0.6_1'
# '1_0_0_0_0'
# '1_1_0_0_0'
# '2_1_0_0_0'
# '1_1_1_0_0'
# '2_1_1_0_0'
# '2_2_1_0_0'
# '3_2_1_0_0'
# '1_1_1_1_0'
# '2_1_1_1_0'
# '2_2_1_1_0'
# '3_2_1_1_0'
# '2_2_2_1_0'
# '3_2_2_1_0'
# '3_3_2_1_0'
# '4_3_2_1_0'
'1_1_1_1_1'
# '2_1_1_1_1'
# '2_2_1_1_1'
# '3_2_1_1_1'
# '2_2_2_1_1'
# '3_2_2_1_1'
# '3_3_2_1_1'
# '4_3_2_1_1'
# '2_2_2_2_1'
# '3_2_2_2_1'
# '3_3_2_2_1'
# '4_3_2_2_1'
# '3_3_3_2_1'
# '4_3_3_2_1'
# '4_4_3_2_1'
# '5_4_3_2_1'
)

name_col1='patients'
name_col2='RDs'

for VS in "${VECTOR_STRINGS[@]}"; do

  cd bin/
  snakemake --snakefile Snakefile.projetmp --cores 22 --config vector_str="$VS"
  # # snakemake --cores 22 --config vector_str=1_0_0_0

  echo "======================================"
  echo " Post-processing Excel outputs for $VS"
  python -m bin.2_concat_ra --filter-type "$VS" --col1 "$name_col1" --col2 "$name_col2" 
 
done

echo " All Snakemake runs + post-processing complete!"

 