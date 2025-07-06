#!/usr/bin/env bash
set -euo pipefail


#############################################
### Define variables
#############################################
user_nb_top_rd=50


# default list, if no args given
VECTOR_STRINGS=(
 '1_1_0_1_0'
 '1_0_0_0_0'
 '1_1_0_0_0'
 '1_1_1_0_0'
 '1_1_1_1_0'
 '1_1_1_1_1'
 '2_1_1_1_1'
 '2_2_1_1_1'
 '2_2_2_1_1'
 '2_2_2_2_1'
 '3_2_2_2_1'
 '3_3_2_2_1'
 '3_3_3_2_1'
 '4_3_3_2_1'
 '4_4_3_2_1'
 '5_4_3_2_1'

# '1_1_0_1_0'
# '1_1_1_0_0'
# '1_1_1_1_0'
# '2_2_1_1_1'
# '2_2_2_1_1'
# '2_2_2_2_1'
# '3_2_2_2_1'
# '3_3_2_2_1'
# '3_3_3_2_1'
# '4_3_3_2_1'
# '4_4_3_2_1'
# '5_4_3_2_1'
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



for VS in "${VECTOR_STRINGS[@]}"; do

    config_rd="resnik_n_all_product4_avril_2025_${VS}"
    echo $config_rd

    cd bin/

    python3 config_rd.py --config_rd "$config_rd"

    cd ../


    python3 -m bin.compare_rslt.1_compare_rank_global --logic_patient "and" # and or rsl_only ra_only
    # # plot dependant RSD and RA 
    # # python3 -m bin.compare_rslt.1_barplot_rank --df_chosen "nan"
    # # python3 -m bin.compare_rslt.1_barplot_rank --df_chosen "no"

    # test stats for the distribution
    python3 -m bin.compare_rslt.2_rank_global
    # # phenotypic profil
    # python3 -m bin.compare_rslt.3_profile_rdi_stat
    # # phenotypic profil
    # python3 -m bin.compare_rslt.3_profile_rd_patient_stat

    # # metric_patient folder no ranking limit and for all methods
    # python3 -m bin.compare_rslt.4_metric_ranking_per_patient


    # # metric_classif folder phenotypic profil + classif top user_nb_top_rd
    # for seed in "${PATIENTS[@]}"; do
    #     echo $seed
    #     python3 -m bin.compare_rslt.5_metric_classif_per_patient --user_nb_top_rd "$user_nb_top_rd" --onep "$seed"

    # done

    # python3 -m bin.compare_rslt.6_make_it_global

    
    python3 -m bin.compare_rslt.8_plot_freq_rdi --col_rank "rank" --add_dot "n" --logic_patient "and"
    python3 -m bin.compare_rslt.8_plot_freq_rdi --col_rank "rank" --add_dot "y" --logic_patient "and"

    python3 -m bin.compare_rslt.8_cdf_auc --dropna "n" --top50 "y" --logic_patient "and"

    python3 -m bin.compare_rslt.10_mean_rank_rdi --topn 50 --logic_patient "and"
    python3 -m bin.compare_rslt.10_mrr_rdi --logic_patient "and"

    # ##################################
    python3 -m bin.compare_rslt.8_plot_freq_rdi --col_rank "rank" --add_dot "n" --logic_patient "or"
    python3 -m bin.compare_rslt.8_plot_freq_rdi --col_rank "rank" --add_dot "y" --logic_patient "or"

    python3 -m bin.compare_rslt.8_cdf_auc --dropna "n" --top50 "y" --logic_patient "or"

    python3 -m bin.compare_rslt.10_mean_rank_rdi --topn 50 --logic_patient "or"
    python3 -m bin.compare_rslt.10_mrr_rdi --logic_patient "or"

    # ##################################

    # ##################################
    python3 -m bin.compare_rslt.8_plot_freq_rdi --col_rank "rank" --add_dot "n" --logic_patient "rsd_only"
    python3 -m bin.compare_rslt.8_plot_freq_rdi --col_rank "rank" --add_dot "y" --logic_patient "rsd_only"

    python3 -m bin.compare_rslt.8_cdf_auc --dropna "n" --top50 "y" --logic_patient "rsd_only"

    python3 -m bin.compare_rslt.10_mean_rank_rdi --topn 50 --logic_patient "rsd_only"
    python3 -m bin.compare_rslt.10_mrr_rdi --logic_patient "rsd_only"

    # ##################################

    # ##################################
    python3 -m bin.compare_rslt.8_plot_freq_rdi --col_rank "rank" --add_dot "n" --logic_patient "ra_only"
    python3 -m bin.compare_rslt.8_plot_freq_rdi --col_rank "rank" --add_dot "y" --logic_patient "ra_only"

    python3 -m bin.compare_rslt.8_cdf_auc --dropna "n" --top50 "y" --logic_patient "ra_only"

    python3 -m bin.compare_rslt.10_mean_rank_rdi --topn 50 --logic_patient "ra_only"

    python3 -m bin.compare_rslt.10_mrr_rdi --logic_patient "ra_only"

    # ##################################

    # # python3 -m bin.compare_rslt.7_barplot_per_patient


    # #python3 -m bin.compare_rslt.9_plot_mean_grp_per_methods

done


    # #python3 -m bin.compare_rslt.8_plot_freq_rdi --col_rank "reciprocal_rank" --add_dot "n"
    # python3 -m bin.compare_rslt.8_cdf_auc --dropna "n" --top50 "y" --logic_patient "and"
    # python3 -m bin.compare_rslt.8_cdf_auc --dropna "n" --top50 "y" --logic_patient "or"
    # python3 -m bin.compare_rslt.8_cdf_auc --dropna "n" --top50 "y" --logic_patient "ra_only"
    # python3 -m bin.compare_rslt.8_cdf_auc --dropna "n" --top50 "y" --logic_patient "rsd_only"




# parallel -j22 --halt soon,fail=1 '
#   VS="{}"
#   config_rd="resnik_n_all_product4_avril_2025_${VS}"

#   cd bin || exit 1

#   python3 config_rd.py --config_rd "$config_rd"
#   cd ..

#   python3 -m bin.compare_rslt.1_compare_rank_global
#   python3 -m bin.compare_rslt.1_barplot_rank
#   python3 -m bin.compare_rslt.2_rank_global
#   python3 -m bin.compare_rslt.3_profile_rdi_stat
#   python3 -m bin.compare_rslt.3_profile_rd_patient_stat
#   python3 -m bin.compare_rslt.4_metric_ranking_per_patient

#   for seed in "${PATIENTS[@]}"; do
#     echo "--- seed: $seed"
#     python3 -m bin.compare_rslt.5_metric_classif_per_patient \
#       --user_nb_top_rd "$user_nb_top_rd" --onep "$seed"
#   done

#   python3 -m bin.compare_rslt.6_make_it_global
#   python3 -m bin.compare_rslt.8_plot_mrr_rdi
#   python3 -m bin.compare_rslt.8_plot_freq_rdi
# ' ::: "${VECTOR_STRINGS[@]}"
 