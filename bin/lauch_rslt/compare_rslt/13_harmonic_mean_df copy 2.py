

from bin.set_log import * 
import re 

from bin.path_variable import (
    PATH_OUTPUT_COMPARE_RSLT,
    PATH_OUTPUT_COMPARE_GLOBAL,
    PATH_OUTPUT_PRODUCT,
    PATH_OUTPUT_DF_PRODUCT7,
)






def get_parent_hierarchy_up_to_level(type_id,df_f,df_pd7,df_all_classif,hierarchy_level=2):
    """
    Get parent classification hierarchy (up to a given level) for a patient's RDI.

    Parameters:
    - type_id: patient type (e.g., 'P0001068')
    - df_f: DataFrame with classification info including 'type', 'is_rdi', 'rd_id'
    - df_pd7: DataFrame to map 'rd_id' to 'Classif_id'
    - df_all_classif: Full classification DataFrame with 'root', 'child_id', 'parent_id', 'parent_type'
    - hierarchy_level: Maximum depth of hierarchy to retrieve (default = 2)

    Returns:
    - group_n_level: List of parent_ids up to the specified hierarchy level
    """

    mini_df = df_f[df_f['type'] == type_id]
    rdi_ids = mini_df.loc[mini_df["is_rdi"] == "y"]["rd_id"].unique()

    if len(rdi_ids) == 0:
        print(f"No RDI found for {type_id}")
        return []

    rdi_pp = df_pd7[df_pd7['ORPHACode'].isin(rdi_ids)]["Classif_id"].values[0]
    df_pd_classif_f_pp = df_all_classif[df_all_classif["root"] == rdi_pp]

    direct_parents = df_pd_classif_f_pp[df_pd_classif_f_pp['child_id'].isin(rdi_ids)]
    direct_parents_list = direct_parents['parent_id'].drop_duplicates().tolist()

    hierarchies = {}

    for parent_id in direct_parents_list:
        parent_type = direct_parents[direct_parents['parent_id'] == parent_id]['parent_type'].values[0]
        current_ids = [parent_id]
        visited = set()
        n = 1
        hierarchy = [(parent_id, parent_type, n)]

        while current_ids:
            next_ids = []
            for cid in current_ids:
                if cid in visited:
                    continue
                visited.add(cid)

                df_child = df_pd_classif_f_pp[df_pd_classif_f_pp['child_id'] == cid]
                rows_c = df_child['child_id'].drop_duplicates().tolist()

                n += 1
                for child in rows_c:
                    pid = df_child[df_child['child_id'] == child]['parent_id'].values[0]
                    ptype = df_child[df_child['child_id'] == child]['parent_type'].values[0]
                    hierarchy.append((pid, ptype, n))
                    next_ids.append(pid)
            current_ids = next_ids

        hierarchies[parent_id] = hierarchy

    group_n_level = []
    for key, parent_list in hierarchies.items():
        for el in parent_list:
            if el[2] <= hierarchy_level:
                group_n_level.append(el[0])
                print(f"For the Direct parent {key} : level {el[2]} → {el[0]}")

    return group_n_level










#############################################################################


logger.info(f"\n\n############################################")
print(f"\n\n############################################")

print(f"START  13_harmonic_mean_df")
logger.info(f"START  13_harmonic_mean_df")

t0 = time.perf_counter()

df_pd7 = pd.read_excel(PATH_OUTPUT_DF_PRODUCT7,index_col=0)


df_global_classif = pd.read_excel(PATH_OUTPUT_COMPARE_GLOBAL + "/global_classif.xlsx",index_col=0)

df_f =  df_global_classif[["type","method","group_id","rd_id","rank","is_rdi","pp_id"]]
df_f = df_f.drop_duplicates()
list_patient = df_f['type'].unique()
list_method =df_f['method'].unique()


###############################################################################

df_all_clasiff =pd.read_excel(PATH_OUTPUT_PRODUCT + "/classifs.xlsx",index_col=0)



"""
Je construis une df en ne gardant que les group  pour les parent et enfant 
enfaite le pp c'est une classif c'est le premier groupe le plus haut dans l'arbre 
"""
    

############################################")############################################")
orphanet_classif_f = {}
list_orphanet_classif = os.listdir(PATH_OUTPUT_PRODUCT_CLASSIF)
for onec in list_orphanet_classif:
    if ".xlsx" in onec:
        classif_name = re.sub(r'^ORPHAclassification_\d+_(.*?)_en_2024\.xlsx$', r'\1', onec)
        orphanet_classif_f[(classif_name.replace("_"," "))] = onec

df_single_classif = df_pd7[['Classif_id',"Classif_name"]].drop_duplicates().dropna()



all_interaction = []
for onep in ["P0001068"]:
    
    ########### turn into function 

    mini_df = df_f[df_f['type'] == onep]
    ## get the RDI
    rdi_ids = mini_df.loc[mini_df["is_rdi"] == "y"]["rd_id"].unique()
    ## get the pp of the RDI 
    rdi_pp = df_pd7[df_pd7['ORPHACode'].isin(rdi_ids)]["Classif_id"].values[0]
    ## get the classif related to the pp 
    df_pd_classif_f_pp = df_all_clasiff[df_all_clasiff["root"] == rdi_pp]

    ## get the direct parent thus the n+1
    direct_parents = df_pd_classif_f_pp[df_pd_classif_f_pp['child_id'] == rdi_ids]
    direct_parents_list = direct_parents['parent_id'].drop_duplicates().tolist()


    ########### turn into function 

    ##  Traverse hierarchy separately for each direct parent
    hierarchies = {}

    # do the hierarchy for each direct parent 
    for row in direct_parents_list:
        parent_id = row
        parent_type = direct_parents[direct_parents['parent_id'] == row]['parent_type'].values[0]
        
        current_ids = [parent_id]
        visited = set()

        n = 1
        hierarchy = [(parent_id, parent_type, n)]  # Initialize with the direct parent
    
        ## recurcivity while current_ids not empty
        while current_ids:
            next_ids = []
        
            for cid in current_ids:
                ## test if we alredy see the RD 
                if cid in visited:
                    continue
                visited.add(cid)
                # Get rows where this ID is a child
                df_child = df_pd_classif_f_pp[df_pd_classif_f_pp['child_id'] == cid]
                rows_c = df_child['child_id'].drop_duplicates().tolist()

                n= n+1 # level of hierarchy
                ## loop for the child of the parent in the current_ids
                for children in rows_c:
                    pid = df_child[df_child['child_id'] == children ]['parent_id'].values[0]
                    ptype = df_child[df_child['child_id'] == children ]['parent_type'].values[0]
                    hierarchy.append((pid, ptype,n))
                    next_ids.append(pid)
            current_ids = next_ids

        hierarchies[parent_id] = hierarchy
    ########### turn into function 
    ## get the n+2 the level of hierachy desired
    group_n_level = []
    for key,list_parent in hierarchies.items():
        for el in list_parent:
            if el[2] <= 2:
                group_n_level.append(el[0])
                print(f"For the Direct parent {key} : get the {el[2]} level {el[0]}")


    ### this is what i will use group_n_level
    # make the calculation for each methods
    for onem in list_method:
        mini_mini_df = mini_df[mini_df['method'] == onem]




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
summary_df.to_excel(PATH_OUTPUT_COMPARE_RSLT + "_hm_rank_group_n_rdi.xlsx")


logger.info(f"END  13_harmonic_mean_df done in {time.perf_counter() - t0:.1f}s")
print(f"END  13_harmonic_mean_df done in {time.perf_counter() - t0:.1f}s")
