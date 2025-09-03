

from bin.set_log import * 
import re 

from bin.path_variable import (
    CONFIG_ALPHA,
    PATH_OUTPUT_HM,
    PATH_OUTPUT_COMPARE_GLOBAL,
    PATH_OUTPUT_PRODUCT,
    PATH_OUTPUT_DF_PRODUCT7,
    PATH_OUTPUT_COMPARE_RSLT
)

### EQUAL PART USELESS 
# def extract_hierarchy_levels_egal(hierarchies, hierarchy_level):
 
#     group_n_level = set()
#     n=0
#     for key, parent_list in hierarchies.items():
#         #logger.info(f"{key} Nb caterogy {len(parent_list)}")
#         # hierarchy_level =int(len(parent_list) / 4) +1

#         for el in parent_list:
#             ## if i want half of the element on the hircrachie 
#             if el[2] == hierarchy_level: ## avec >= le rslt change 
#                 group_n_level.add(el[0])
#             # else the hierarchy_level is not available of the classif of RD thus we take the max (which ill be obvsouily less but still usefull)
#             elif el[2] == len(parent_list):
#                 group_n_level.add(el[0])
#                 n=n+1
#     logger.info(f"{n} element on domains have the depth smaller than {hierarchy_level}")
#     return group_n_level
 

 

def extract_hierarchy_levels(hierarchies, hierarchy_level):
    """
    Extract parent IDs from a hierarchy dictionary up to a specific level.

    Parameters:
    - hierarchies: dict with structure {parent_id: [(parent_id, parent_type, level), ...]}
    - hierarchy_level: maximum level to keep (e.g., 2)

    Returns:
    - group_n_level: list of parent_ids up to the given hierarchy level
    """
    group_n_level = set()
    for key, values in hierarchies.items():
        #logger.info(f"{key} Nb caterogy {len(parent_list)}")
        for el in values:
            ## if the level lim is bigger than the level of the rd we add 
            if el[2] <= hierarchy_level  :
                group_n_level.add(el[0])
    return group_n_level

def get_parent_hierarchy_up_to_level(onep,rdi_ids,rdi_classif,df_all_classif,hierarchy_level):
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


    ## get the RDI
    if len(rdi_ids) == 0:
        logger.info(f"No RDI found for {onep}")
        return []
    
    ## get the hirarchie of each classif
    dict_classif = {}
    all_group = []
    for one_classif in rdi_classif:
         
        ## get the classif related to the pp 
        df_pd_classif_f_pp = df_all_classif[df_all_classif["root"] == one_classif]

        ## get the direct parent thus the n+1
        direct_parents = df_pd_classif_f_pp[df_pd_classif_f_pp['child_id'].isin(rdi_ids)]
        direct_parents_list = direct_parents['parent_id'].drop_duplicates().tolist()

        ##  Traverse hierarchy separately for each direct parent
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
        
        dict_classif[one_classif] = hierarchies
        group_n_level = extract_hierarchy_levels(hierarchies, hierarchy_level)
        all_group = all_group + list(group_n_level)

    return dict_classif,all_group


def RD_get_parent_hierarchy_up_to_level(onep,rdi_ids,rdi_classif,df_all_classif,hierarchy_level):
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


    ## get the RDI
    if len(rdi_ids) == 0:
        print(f"No RDI found for {onep}")
        return []
    ## get the hirarchie of each classif
    dict_classif = {}
    all_group = []
    for one_classif in rdi_classif:
         
        ## get the classif related to the pp 
        df_pd_classif_f_pp = df_all_classif[df_all_classif["root"] == one_classif]

        ## get the direct parent thus the n+1
        direct_parents = df_pd_classif_f_pp[df_pd_classif_f_pp['child_id'].isin(rdi_ids)]
        direct_parents_list = direct_parents['parent_id'].drop_duplicates().tolist()

        ##  Traverse hierarchy separately for each direct parent
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
        
        dict_classif[one_classif] = hierarchies
        group_n_level = extract_hierarchy_levels(hierarchies, hierarchy_level)
        all_group = all_group + list(group_n_level)

    return dict_classif,all_group








logger.info(f"\n\n############################################")
print(f"\n\n############################################")

print(f"START  13_harmonic_mean_df")
logger.info(f"START  13_harmonic_mean_df")

t0 = time.perf_counter()

#########################################################################
# # # Set up argument parsing
# parser = argparse.ArgumentParser(description="Process inputs for the script.")

# # # Arguments 
# parser.add_argument("--topn",type=int,required=True,)
# parser.add_argument("--hierarchy_level",type=int,required=True,)

# # # Parse the arguments
# args = parser.parse_args()

# topn = args.topn  
# hierarchy_level = args.hierarchy_level  
########################################################################

## P0012729,P0010577,P0017242 
topn = 10
hierarchy_level =  2
#############################################################################

# df_pd7 = pd.read_excel(PATH_OUTPUT_DF_PRODUCT7,index_col=0)
PATH_OUTPUT_COMPARE_GLOBAL = '/home/maroua/Bureau/my_pipeline_v3/GSSM_DRW/output/compare_rank_1_1_1_1_1_concat_matrix_0.3/global'

df_global_classif = pd.read_excel(PATH_OUTPUT_COMPARE_GLOBAL + "/global_classif.xlsx",index_col=0)

df_f =  df_global_classif[["type","method","group_id","rd_id","rank","is_rdi"]]
df_f = df_f.drop_duplicates()
list_patient = df_f['type'].unique()
list_method =df_f['method'].unique()


###############################################################################

df_all_clasiff =pd.read_excel(PATH_OUTPUT_PRODUCT + "/classifs.xlsx",index_col=0)

list_type_gprd = ["Clinical group","Category"]

# df_all_clasiff[df_all_clasiff['parent_id'].isin(group_n_level) & ~ ( df_all_clasiff["child_type"].isin(list_type_gprd )) ]['child_id'].drop_duplicates().to_list()
# df_all_clasiff[df_all_clasiff['parent_id'].isin(group_n_level) & ~ ( df_all_clasiff["child_type"].isin(list_type_gprd )) ]['root'].drop_duplicates().to_list()


"""
Je construis une df en ne gardant que les group  pour les parent et enfant 
enfaite le pp c'est une classif c'est le premier groupe le plus haut dans l'arbre 
"""




all_interaction = []
for onep in list_patient: # list_patient
    
    print(f'{onep}')
    mini_df = df_f[df_f['type'] == onep]
    rdi_ids = mini_df.loc[mini_df["is_rdi"] == "y"]["rd_id"].unique()
    rdi_id = rdi_ids[0]

    ## get the pp of the RDI 
    # rdi_pp = df_pd7[df_pd7['ORPHACode'].isin(rdi_ids)]["Classif_id"].values[0]
    rdi_classif = df_global_classif[df_global_classif['rd_id'].isin(rdi_ids)]["classif_id"].drop_duplicates().tolist()
    ##  Identify  groups of the RDI
    hierarchies,group_n_level = get_parent_hierarchy_up_to_level(onep,rdi_ids, rdi_classif ,df_all_clasiff,hierarchy_level)
    group_n_level = set(group_n_level)
 

    # hierarchies_equal,group_n_level_equal =  get_parent_hierarchy_up_to_level(onep,rdi_ids, df_pd7 ,df_all_clasiff,hierarchy_level,'y')


    ### this is what i will use group_n_level
    # make the calculation for each methods
    for onem in list_method:
        succes = 0
        ## to filter the RARW 
        if  onem == "RARW":
            onem_f = f"RARW_{CONFIG_ALPHA}"
        else:
            onem_f = onem


        mini_mini_df = mini_df[mini_df['method'] == onem]


        # #### RANKS RD SAME GROUPE N1 NO PP 
        # ## get the RDI group 
        # list_rdi_groups = mini_mini_df[mini_mini_df["rd_id"].isin(rdi_ids)]['group_id'].unique()
        # ## get the RD with the same group as rdi (including the rdi )
        # rd_match_group_rdi = mini_mini_df[mini_mini_df['group_id'].isin(list_rdi_groups)]['rd_id'].unique()
        # ## get the df 
        # df_match_group_rdi = mini_mini_df[(mini_mini_df['rd_id'].isin(rd_match_group_rdi)) & mini_mini_df['group_id'].isin(list_rdi_groups)].drop_duplicates()
        # ## get the rank of each RDs in df format
        # df_for_hm = df_match_group_rdi[['rd_id','rank']].drop_duplicates()
        # ## extract ranks
        # ranks_gp = df_for_hm['rank']


        #### RDI
        df_match_group_rdi_only_rdi = mini_mini_df[mini_mini_df['is_rdi'] == "y"]
        df_for_hm_rdi = df_match_group_rdi_only_rdi[['rd_id','rank']].drop_duplicates()
        ranks_rdi = df_for_hm_rdi['rank'].values[0]
        # print(f"{onep} - {onem_f}\t RDI : {rdi_id} rank {ranks_rdi}")

        ##### LEVEL INFERIEUR OU EGAL A LIMIT 
        ##### RANKS RD SAME GROUP N2 PP RDI
        ## filter keep only top 10
        # mini_mini_df = mini_mini_df[mini_mini_df['rank'] <= topn]
        ## get the rd of the top 10
        # list_rd_top10 = mini_mini_df_topn['rd_id'].drop_duplicates().tolist()

        rd_match_group_rdi = mini_mini_df[mini_mini_df['group_id'].isin(group_n_level)]['rd_id'].unique()
        df_match_group_rdi = mini_mini_df[mini_mini_df['rd_id'].isin(rd_match_group_rdi)].drop_duplicates()

        nb_group_match = mini_mini_df[mini_mini_df['group_id'].isin(group_n_level)]['group_id'].drop_duplicates().tolist()

        # get the rank of each RDs
        df_for_hm = df_match_group_rdi[['rd_id','rank']].drop_duplicates()
        # extract ranks
        ranks_gp = df_for_hm['rank']

        # get the rank of each RDs
        df_for_hm = df_match_group_rdi[['rd_id','rank']].drop_duplicates()
        # extract ranks
        ranks_gp = df_for_hm['rank']


        try:
            # hm
            h_mean_rd_same_group_rdi = len(ranks_gp) / sum(1.0 / r for r in ranks_gp)
 
            # print(f"{onep} - {onem}\tHarmonic mean (manual calculation): {h_mean_rd_same_group_rdi}")
        except ZeroDivisionError:
            h_mean_rd_same_group_rdi = 0
            print(f"{onep} - {onem}\t ZeroDivisionError")
        
        if len(nb_group_match) != 0:
            succes = 1
        else:
            succes = 0

        for onerd in rd_match_group_rdi:
            for onegroup in nb_group_match:
                rank_rd = df_match_group_rdi[df_match_group_rdi['rd_id']==onerd]['rank'].unique()[0]
                classif_related = df_all_clasiff[df_all_clasiff['parent_id']==onegroup]['root'].values[0]
                classif_related_name = df_all_clasiff[df_all_clasiff['parent_id']==onegroup]['root_name'].values[0]

                all_interaction.append((onep,onem_f,succes,onerd,rank_rd,onegroup,len(group_n_level),classif_related,classif_related_name,h_mean_rd_same_group_rdi,rdi_id,ranks_rdi))

df_al_m = pd.DataFrame(all_interaction,columns=['patient','method',"succes","rd","rank_rd","group_id_match","nb_group_tot_rdi","classif_id",'classif_name',"hm_rank_match_group","rdi","rank_rdi"]) #'hm_group_without_rdi'])

df_al_m.to_excel(f"{PATH_OUTPUT_HM}/info/hm_each_patient_{CONFIG_ALPHA}_{hierarchy_level}.xlsx")

  
# ## verification manuelle 
# # df_al_m_f[(df_al_m_f['patient'] == "P0001068") & (df_al_m_f['method'] == "RARW_0.8") ]

# df_al_m_f = df_al_m[df_al_m['succes'] == 1]

# df_mean = df_al_m[["patient","method",'rd',"rank_rd"]].drop_duplicates()
# result = (
#     df_mean.groupby('method')['rank_rd']
#     .agg(
#         mean_arithmetic='mean',
#         mean_harmonic=lambda x: hmean(x) if all(x > 0) else None
#     )
#     .reset_index()
# )


# df_hm_mean = df_al_m[["patient","method",'hm_rank_match_group']].drop_duplicates()
# result_goup = (
#     df_hm_mean.groupby('method')['hm_rank_match_group']
#     .agg(
#         mean_arithmetic='mean',
#         mean_harmonic=lambda x: hmean(x) if all(x > 0) else None
#     )
#     .reset_index()
#     .rename(columns={'mean_harmonic': 'mean_harmonic_harmonic'})
#     .rename(columns={'mean_arithmetic': 'mean_harmonic_arithmetic'})

# )


# ## Same but only for rdi (no top n)
# df_hm_rdi = df_al_m[["patient","method",'rank_rdi',"rdi"]].drop_duplicates()
# result_RDI = (
#     df_hm_rdi.groupby('method')['rank_rdi']
#     .agg(
#         mean_arithmetic='mean',
#         mean_harmonic=lambda x: hmean(x) if all(x > 0) else None
#     )
#     .reset_index()
#     .rename(columns={'mean_harmonic': 'mean_harmonic_rdi'})
#     .rename(columns={'mean_arithmetic': 'mean_arithmetic_rdi'})
# )

# summary_df = result.merge(result_goup, on='method').merge(result_RDI, on='method')


# summary_df.to_excel(f"{PATH_OUTPUT_HM}/hm_{CONFIG_ALPHA}_{hierarchy_level}_{topn}.xlsx")

# logger.info(f"END  13_harmonic_mean_df done in {time.perf_counter() - t0:.1f}s")
 