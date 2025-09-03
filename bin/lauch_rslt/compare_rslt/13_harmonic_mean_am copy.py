from bin.set_log import * 
import re 

from bin.path_variable import (
    PATH_OUTPUT_COMPARE_RSLT,
    PATH_OUTPUT_COMPARE_GLOBAL,
    PATH_OUTPUT_PRODUCT,
    PATH_OUTPUT_DF_PRODUCT7,
)
logger.info(f"\n\n############################################")
print(f"\n\n############################################")

print(f"START  13_harmonic_mean_df")
logger.info(f"START  13_harmonic_mean_df")

t0 = time.perf_counter()

df_pd7 = pd.read_excel(PATH_OUTPUT_DF_PRODUCT7,index_col=0)


df_global_classif = pd.read_excel(PATH_OUTPUT_COMPARE_GLOBAL + "/global_classif.xlsx",index_col=0)

df_f =  df_global_classif[["type","method","group_id","rd_id","rank","is_rdi"]]
df_f = df_f.drop_duplicates()
list_patient = df_f['type'].unique()
list_method =df_f['method'].unique()


############################################")############################################")


df_clasif_only_group = pd.read_excel(PATH_OUTPUT_PRODUCT + "/classif_only_group.xlsx",index_col=0)

"""
Je construis une df en ne gardant que les group  pour les parent et enfant 
enfaite le pp c'est une classif c'est le premier groupe le plus haut dans l'arbre 
"""
    

############################################")############################################")



all_interaction = []
for onep in list_patient : #["P0001068"]:
    mini_df = df_f[df_f['type'] == onep]
    # get the RDI
    rdi_ids = mini_df.loc[mini_df["is_rdi"] == "y"]["rd_id"].unique()
    # get the pp of the RDI 
    rdi_pp = df_pd7[df_pd7['ORPHACode'].isin(rdi_ids)]["Classif_id"].values[0]
    ## get the group related to the pp 
    list_goup_pp = df_clasif_only_group[df_clasif_only_group["root_group_id"] == rdi_pp]['group_id'].drop_duplicates().tolist()

    

    # print(f'{onep} - {rdi_ids}\tNb of group of the pp {rdi_pp} \t {len(list_goup_pp)}')
    # make the calculation for each methods
    for onem in list_method:
        mini_mini_df = mini_df[mini_df['method'] == onem]
        ## get the RDI group 
        list_rdi_groups = mini_mini_df[mini_mini_df["rd_id"].isin(rdi_ids)]['group_id'].unique()
        ## get the RD with the same group as rdi (including the rdi )
        rd_match_group_rdi = mini_mini_df[mini_mini_df['group_id'].isin(list_rdi_groups)]['rd_id'].unique()
        ## get the df 
        df_match_group_rdi = mini_mini_df[(mini_mini_df['rd_id'].isin(rd_match_group_rdi)) & mini_mini_df['group_id'].isin(list_rdi_groups)].drop_duplicates()
        ## get the rank of each RDs in df format
        df_for_hm = df_match_group_rdi[['rd_id','rank']].drop_duplicates()
        ## extract ranks
        ranks_gp = df_for_hm['rank']


        ##### preferentiel parent 
        # get the RD with the same pp and have the same group from the pp as rdi (including the rdi )
        # rd_match_pp_rdi = mini_mini_df[mini_mini_df['pp_id'] == rdi_pp]['rd_id'].unique()
        rd_match_pp_rdi = mini_mini_df[mini_mini_df['group_id'].isin(list_goup_pp)]['rd_id'].unique()
        """ Remarque si je prend le pp c'est celui de la rdi lorsque je le fait matcher avec les rd je me base que sur le ppi de la rdi alors que si je prend tout les group du pp et j'extrait les rd je vais forcement en avoir plus """
        ## get the df 
        df_match_pp_rdi = mini_mini_df[(mini_mini_df['rd_id'].isin(rd_match_pp_rdi)) ].drop_duplicates()
        ## get the rank of each RDs in df format
        df_for_hm_pp = df_match_pp_rdi[['rd_id','rank']].drop_duplicates()
        ## extract ranks pp 
        ranks_pp = df_for_hm_pp['rank']
        ## parfois il se peut que le parent pp de la rdi 


        ## for rank rdi 
        df_match_group_rdi_only_rdi = df_match_group_rdi[df_match_group_rdi['is_rdi'] == "y"]
        df_for_hm_rdi = df_match_group_rdi_only_rdi[['rd_id','rank']].drop_duplicates()
        ## extract ranks
        ranks_rdi = df_for_hm_rdi['rank'].values[0]
        
        logger.info(f"{onep} - {onem}\t RDI : {rdi_ids} rank {ranks_rdi}")
        logger.info(f"{onep} - {onem}\t RDs match group RDI  - Nb  {len(ranks_gp)} ")

        # calculate the harmonic rank 
        try:
            # hm
            h_mean_rd_same_group_rdi = len(ranks_gp) / sum(1.0 / r for r in ranks_gp)
            logger.info(f"{onep} - {onem}\tHarmonic mean (manual calculation) for rd same group RDI: {h_mean_rd_same_group_rdi}")
        except ZeroDivisionError:
            h_mean_rd_same_group_rdi = 0
            # h_mean_rd_same_group_no_rdi = 0
            print(f"{onep} - {onem}\t ZeroDivisionError")


        # calculate the harmonic rank 
        try:
            # pp THIS should be an except error !!!
            h_mean_rd_same_pp_rdi = len(ranks_pp) / sum(1.0 / r for r in ranks_pp)
            logger.info(f"{onep} - {onem}\tHarmonic mean (manual calculation) for rd same pp RDI: {h_mean_rd_same_pp_rdi}")
        except ZeroDivisionError:
            h_mean_rd_same_pp_rdi = np.nan
            # h_mean_rd_same_group_no_rdi = 0
            print(f"{onep} - {onem}\t ZeroDivisionError")

        #for oner in ranks_gp:
        all_interaction.append((onep,onem,h_mean_rd_same_pp_rdi,h_mean_rd_same_group_rdi,ranks_rdi)) #h_mean_rd_same_group_no_rdi ranks_rdi

df_hm_general_nof = pd.DataFrame(all_interaction,columns=['patient','method','hm_rd_same_pp','hm_rd_same_groupe','rank_rdi']) #'hm_group_without_rdi'])
patient_before = df_hm_general_nof["patient"]
df_hm_general = df_hm_general_nof.dropna()
patient_after = df_hm_general["patient"].drop_duplicates()
lack_patient = set(patient_before).difference(patient_after)


logger.info(f" {len(lack_patient)} don't have RDI in the pd4 -> REMOVED ")
# df_hm_general.to_excel('hm_general.xlsx')

df_hm_rdi  = df_hm_general[['patient','method','rank_rdi']].drop_duplicates()
df_hm_group  = df_hm_general[['patient','method','hm_rd_same_groupe']]
df_hm_pp  = df_hm_general[['patient','method','hm_rd_same_pp']]


# 1 Compute the average HM hm_rd_same_groupe
mean_hm_group = (
    df_hm_group
    .groupby('method', as_index=False)['hm_rd_same_groupe']
    .mean()
    .rename(columns={'hm_rd_same_groupe': 'mean_hm_rd_same_groupe'})
)

# 2. Harmonic mean of hm_rd_same_groupe
harmonic_hm_group = (
    df_hm_group
    .groupby('method', as_index=False)['hm_rd_same_groupe']
    .agg(hm_hm_rd_same_groupe=hmean)
)

# 3.Compute the average HM hm_rd_same_pp
mean_hm_pp = (
    df_hm_pp
    .groupby('method', as_index=False)['hm_rd_same_pp']
    .mean()
    .rename(columns={'hm_rd_same_pp': 'mean_hm_rd_same_pp'})
)

# 4. Harmonic mean of hm_rd_same_pp
harmonic_hm_pp = (
    df_hm_pp
    .groupby('method', as_index=False)['hm_rd_same_pp']
    .agg(hm_hm_rd_same_pp=hmean)
)

# 5. Harmonic mean of rank_rdi
harmonic_rank = (
    df_hm_rdi
    .groupby('method', as_index=False)['rank_rdi']
    .agg(hm_rank_rdi=hmean)
)

# Merge all into one DataFrame
summary_df = mean_hm_group.merge(harmonic_hm_group, on='method').merge(harmonic_rank, on='method').merge(mean_hm_pp, on='method').merge(harmonic_hm_pp, on='method')




################################################

df_compare = pd.read_excel(PATH_OUTPUT_COMPARE_RSLT + "/" + "compare_rank_method.xlsx",index_col=0)
df_compare = df_compare.dropna()
all_interecation = []
rank_method = df_compare['RSD'].astype(float)
harmonic_mean = len(rank_method) / (1.0 / rank_method).sum()
all_interecation.append(('RSD',harmonic_mean))
rank_method = df_compare['RA'].astype(float)
harmonic_mean = len(rank_method) / (1.0 / rank_method).sum()
all_interecation.append(('RA',harmonic_mean))
rank_method = df_compare['RARW'].astype(float)
harmonic_mean = len(rank_method) / (1.0 / rank_method).sum()
all_interecation.append(('RARW',harmonic_mean))

df_hm_general_2 = pd.DataFrame(all_interecation,columns=['method','CR_hm_rank_rdi'])  



summary_df = summary_df.merge(df_hm_general_2, on='method', how='left')
# summary_df.to_excel(PATH_OUTPUT_COMPARE_RSLT + "_hm_rank_group_n_rdi.xlsx")


logger.info(f"END  13_harmonic_mean_df done in {time.perf_counter() - t0:.1f}s")
print(f"END  13_harmonic_mean_df done in {time.perf_counter() - t0:.1f}s")
