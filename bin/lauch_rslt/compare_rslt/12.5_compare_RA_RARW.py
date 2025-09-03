

from bin.set_log import *

PATH_OUTPUT_COMPARE_GLOBAL = '/home/maroua/Bureau/wip/my_pipeline_v2/output//compare_rank_1_1_1_1_1_concat_matrix_0.3//global/'
df = pd.read_excel(PATH_OUTPUT_COMPARE_GLOBAL + "/global_classif.xlsx",index_col=0)

df = df[df['method'].isin(["RA","RARW"])]
list_patient = df['type'].unique()
list_method = df['method'].unique()

# store all the subdf 
all_dfs = []

# P0012825
for onep in  list_patient:
    mini_df = df[df['type'] == onep]
    # get the RDI
    rdi_ids = mini_df.loc[mini_df["is_rdi"] == "y", "rd_id"].unique()

    # make the calculation for each methods

    for onem in list_method:
        ## filter per methods
        mini_mini_df = mini_df[mini_df['method'] == onem]
        ## filter to top N
        # mini_mini_df_filter_rank = mini_mini_df[mini_mini_df['rank'] <= 15]
        # get the RDI group 
        list_rdi_groups = mini_mini_df[mini_mini_df["rd_id"].isin(rdi_ids)]['group_id'].unique()
        # get the RD with the same group as rdi (including the rdi )
        rd_match_group_rdi = mini_mini_df[mini_mini_df['group_id'].isin(list_rdi_groups)]['rd_id'].unique()

        # get the df 
        df_match_group_rdi = mini_mini_df[mini_mini_df['rd_id'].isin(rd_match_group_rdi)].drop_duplicates()

        # get the rank of each RDs in df format
        df_for_hm = df_match_group_rdi[["type","method",'rd_id','rank',"is_rdi"]].drop_duplicates()
        
        nb_rd = len(df_for_hm)
 

        df_for_hm['nb_rd'] = nb_rd
        # df_for_hm['type'] = str(f"P{i}")

        all_dfs.append(df_for_hm)
    i=i+1

final_df = pd.concat(all_dfs, ignore_index=True)
# final_df.to_excel('final_compare_ra_rw_no_group.xlsx')
# final_df.to_excel('final_compare_ra_rw.xlsx')
# First, group the metrics by patient

final_df
# P0012825
for onep in  list_patient:
    mini_df = final_df[final_df['type'] == onep]
    mini_df = mini_df[mini_df['rank'] <= 20]
    try:
        nb_rd_ra = mini_df[mini_df['method'] == 'RA']['nb_rd'].values[0]
    except IndexError:
        nb_rd_ra = 0
    try:
        nb_rd_rarw = mini_df[mini_df['method'] == 'RARW']['nb_rd'].values[0]
    except IndexError:
        nb_rd_rarw = 0
    if nb_rd_rarw > nb_rd_ra:
        print(f"{onep}\t RARW more nb : {nb_rd_rarw}\t {nb_rd_rarw} - {nb_rd_ra} = {nb_rd_rarw-nb_rd_ra}")
    if nb_rd_rarw == nb_rd_ra:
        print(f"{onep}\t Same nb : {nb_rd_rarw}\t {nb_rd_rarw} ")



df = final_df

summary_list = []

for patient in df['type'].unique():
    sub = df[df['type'] == patient]

    # Only keep rd_id present in both methods (RA & RARW)
    counts = sub['rd_id'].value_counts()
    rd_common_ids = counts[counts == 2].index  # must appear twice (once per method)
    rd_common = sub[sub['rd_id'].isin(rd_common_ids)]

    # Pivot for comparison
    wins = rd_common.pivot(index='rd_id', columns='method', values='rank')

    # Safely check for both columns
    ra_col = 'RA' in wins.columns
    rarw_col = 'RARW' in wins.columns
    if ra_col and rarw_col:
        n_win_RA = (wins['RA'] < wins['RARW']).sum()
        n_win_RARW = (wins['RARW'] < wins['RA']).sum()
    else:
        n_win_RA = 0
        n_win_RARW = 0

    # nb_rd per method
    nb_rd_RA = sub[sub['method'] == 'RA']['nb_rd'].iloc[0] if not sub[sub['method'] == 'RA'].empty else None
    nb_rd_RARW = sub[sub['method'] == 'RARW']['nb_rd'].iloc[0] if not sub[sub['method'] == 'RARW'].empty else None

    # Winner logic
    if n_win_RA > n_win_RARW:
        winner = 'RA'
    elif n_win_RARW > n_win_RA:
        winner = 'RARW'
    else:  # Tie in n_win, tiebreak on nb_rd
        if (nb_rd_RA is not None and nb_rd_RARW is not None):
            if nb_rd_RA > nb_rd_RARW:
                winner = 'RA'
            elif nb_rd_RARW > nb_rd_RA:
                winner = 'RARW'
            else:
                winner = 'tie'
        else:
            winner = 'unknown'
    
    summary_list.append({
        'type': patient,
        'nb_rd_RA': nb_rd_RA,
        'nb_rd_RARW': nb_rd_RARW,
        'n_win_RA': n_win_RA,
        'n_win_RARW': n_win_RARW,
        'winner': winner
    })

summary_df = pd.DataFrame(summary_list)
# summary_df.to_excel("AAA.xlsx")






#ORPHA:199
## evaluation process
method_m = "RARW"
rdi= df[(df['type'] == "P0007806" )& (df["is_rdi"]=="y")& (df["method"]==method_m)]['rd_id'].values[0]

group_rdi = df[(df['type'] == "P0007806" )& (df["method"]==method_m) & (df["rd_id"]==rdi)]['group_id'].drop_duplicates().tolist()

df_ff = df[(df['type'] == "P0007806" )& (df["method"]==method_m) & (df["group_id"].isin(group_rdi))].drop_duplicates()
df_ff['rd_id'].drop_duplicates().tolist()
len(df_ff['rd_id'].drop_duplicates().tolist())
#################################################
"""
## OLD VERSION 

summary_df = pd.read_excel(PATH_OUTPUT_COMPARE_RSLT + 'summary_df.xlsx')  


df_compare_ra_rarw = summary_df[['patient','method','RDI_rd_id',"RDI_rank","candidate_rd_id","candidate_rank"]] 
df_compare_ra_rarw = df_compare_ra_rarw[df_compare_ra_rarw['method'].isin(["RA","RARW"])]
patient_list = df_compare_ra_rarw['patient'].drop_duplicates().tolist()

for onep in patient_list:
    print(onep)
    mini_df = df_compare_ra_rarw[df_compare_ra_rarw['patient'] == onep]
   
    ## 2. Determine which method has the best (lowest) global-RD rank
    confirmed = mini_df[['method', 'RDI_rank']].drop_duplicates()
    best_method = confirmed.loc[confirmed['RDI_rank'].idxmin(), 'method']
    print(f"Method with best confirmed-RD rank: {best_method}")

    ## 3. Compute mean candidate_rank of the top 20 candidates per method
    # sort the ranking 
    top20 = (
        mini_df.sort_values('candidate_rank')
        .groupby('method')
        .head(20)
    )
    # mean_top20 = top20.groupby('method')['candidate_rank'].mean()
    # print("\nMean candidate_rank (top 20) per method:")
    # print(mean_top20.to_string())

    # 4. Compute global mean candidate_rank per method
    mean_global = mini_df.groupby('method')['candidate_rank'].mean()
    print("\nMean candidate_rank (global) per method:")
    print(mean_global.to_string())

    # # 5. Compare the RA vs RARW differences
    # diff_top20 = abs(mean_top20['RA'] - mean_top20['RARW'])
    # diff_global = abs(mean_global['RA'] - mean_global['RARW'])
    # best_metric = 'Top 20 average' if diff_top20 > diff_global else 'Global average'
    # print(f"\nMetric with the largest RA vs RARW difference: {best_metric}")


 
    # 2. Define the list of "top N" thresholds you want to test
    Ns = [5, 10, 15, 20, 25, 30]

    # 3. Loop over each cutoff, count distinct ORPHA per method, and report the winner
    results = []
    for n in Ns:
        topn = mini_df[mini_df['candidate_rank'] <= n]
        counts = topn.groupby('method')['candidate_rd_id'].nunique()
        # Fill missing methods with 0
        ra_count   = counts.get('RA', 0)
        rarw_count = counts.get('RARW', 0)
        winner = 'RARW' if rarw_count > ra_count else ('RA' if ra_count > rarw_count else 'Tie')
        results.append({'top_n': n,
                        'RA': ra_count,
                        'RARW': rarw_count,
                        'winner': winner})

    # 4. Display results
    for row in results:
        print(f"Top {row['top_n']:2d}:  RA={row['RA']:3d},  RARW={row['RARW']:3d}  →  Winner: {row['winner']}")


    print("###############################")


"""