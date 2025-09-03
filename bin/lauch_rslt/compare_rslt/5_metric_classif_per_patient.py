
from bin.set_log import * 
from bin.path_variable import (
    PATH_OUTPUT_COMPARE_METRIC_CLASSIF,
    PATH_OUTPUT_DF_PRODUCT1,
    PATH_OUTPUT_DF_PC_CLASSIF,
    PATH_OUTPUT_PRODUCT_CLASSIF,
    PATH_OUTPUT_COMPARE_RSLT_PER_PATIENT
)



def get_name_rype_pd1(pd1,rd_oi):
    try: 
        rd_name = pd1[pd1['ORPHACode'] == rd_oi]['Name'].values[0]
        rd_type = pd1[pd1['ORPHACode'] == rd_oi]['Group'].values[0]
    except IndexError:
        rd_name = ""
        rd_type = ""
    return rd_name,rd_type 

def similarity_word(a, b):
    """Return a similarity ratio between two strings using difflib."""
    return SequenceMatcher(None, a, b).ratio()


def get_related_group_pp_json(dict_append,name_method_json_key,rank_method,get_pp_step,list_rd_step,pd_orphanet_classif_xlsx):
    dict_append[name_method_json_key] = {}

    try:
        rank_method = int(rank_method )
    except ValueError:
        rank_method = np.nan

    # 1. Collect RD information.
    rd_info = {}
    for one_rd in list_rd_step:
        try:
            rd_name, rd_type = get_name_rype_pd1(df_pd1, one_rd)
        except IndexError:
            print(f"{one_rd} not in the pd1 no name and type found")
            print(f" /!\ IndexError  /!\  {one_rd} not in the pd1 no name and type found")
            rd_name = ""
            rd_type = ""

        rd_info[one_rd] = {"name": rd_name, "type": rd_type}

    dict_append[name_method_json_key] =  {
                    "rank_rdi" : rank_method,
                    "RD": rd_info,
                    "count": len(rd_info),
                }


    # 2. Match each motif (preferred parent classification name) with the best matching xlsx file.
    best_matches = {}
    for motif in get_pp_step:
        best_file = ""
        best_score = 0
        # Compare each classification file (xlsx) against the motif.
        for file_name in pd_orphanet_classif_xlsx:
            score = similarity_word(motif.lower(), file_name.lower())
            if score > best_score:
                best_score = score
                best_file = file_name
        best_matches[motif] = best_file

    list_classif_f = []  # will accumulate one entry per motif

    for key_m, excel_file in best_matches.items():
        # Load the classification DataFrame for this motif.
        df_pd_classif = pd.read_excel(os.path.join(PATH_OUTPUT_PRODUCT_CLASSIF, excel_file), index_col=0)

        # Collect unique interactions as tuples: (rd, related_group)
        interaction_rd = set()
        # add rdi in the list to make comparaison
        #list_rd_step.append(rdi)
        # For each RD in our list, get related groups from both the child and parent positions.
        for one_rd in list_rd_step:
            child_df = df_pd_classif[df_pd_classif['child_id'] == one_rd]
            for parent_of_one_rd in child_df["parent_id"].tolist():
                interaction_rd.add((one_rd, parent_of_one_rd))
            parent_df = df_pd_classif[df_pd_classif['parent_id'] == one_rd]
            for child_of_one_rd in parent_df["child_id"].tolist():
                interaction_rd.add((one_rd, child_of_one_rd))
        
        # Group the interactions by the related group identifier.
        groupe_by_classif = {}
        for rd, group in interaction_rd:
            groupe_by_classif.setdefault(group, []).append(rd)
        
        # Build a list of group dictionaries for the current motif.
        list_classif = []  
        for key_classif, rd_list in groupe_by_classif.items():
            # Create a new dictionary for each group.
            gp_name, gp_type = get_name_rype_pd1(df_pd1, key_classif)
            group_entry = {
                "classif": {
                    "id": key_classif,
                    "name": gp_name,
                    "type": gp_type,
                    "count": len(rd_list),
                    "RD": []  # to hold a list of RD dictionaries
                }
            }
            # Populate the list of related RD.
            for rd_v in rd_list:
                gp_name_v, gp_type_v = get_name_rype_pd1(df_pd1, rd_v)
                rd_info = {
                    "id": rd_v,
                    "name": gp_name_v,
                    "type": gp_type_v
                }
                group_entry["classif"]["RD"].append(rd_info)
            list_classif.append(group_entry)
        
        # Build an entry for this motif which includes a preferred parent classification "name"
        # along with all its grouped RD.
        motif_entry = {
            "classif_name": {
                "name": key_m,
                "id" : df_pd_classif['root'].values[0],
                "count":int(len(groupe_by_classif.keys())),
                "RD": list_classif
            }
        }
        list_classif_f.append(motif_entry)

    # Add the accumulated information into the result dictionary.
    dict_append[name_method_json_key]["Matching_pp"] = {"count" : len(list_classif_f)-1,
                                                        "elements" : list_classif_f}
    return dict_append



####################################################################################


def from_json_to_df_classif(df_metric_ranking,onep,rdi,json_dict,method_name,rslt_tuple):

    method_section = json_dict[method_name]
    classif_count = method_section['Matching_pp']['count']
    list_classif_rd = method_section['Matching_pp']['elements']
    
    for oneclassif in list_classif_rd:
        classif_name = oneclassif['classif_name']['name']
        classif_id = oneclassif['classif_name']['id']
        classif_nb_rd_related = oneclassif['classif_name']['count']
        list_rd_from_group =oneclassif['classif_name']['RD']
        for onegrp in list_rd_from_group:
            group_id = onegrp['classif']['id']
            group_name = onegrp['classif']['name']
            group_count = onegrp['classif']['count']
            list_group_rd_match =  onegrp['classif']['RD']
            #if group_count >= 1:
            for oneRD in list_group_rd_match:
                rd_id = oneRD["id"]
                if rd_id == rdi:
                    #print(f"{onep}\trdi : {rdi}")
                    is_rdi = 'y'
                    rank = json_dict[method_name]['rank_rdi']

                else:
                    is_rdi = 'n'
                    rank = df_metric_ranking[df_metric_ranking["ORPHAcode"]==rd_id]['rank'].astype(int).values[0]
                rd_name = oneRD["name"]
                rd_type = oneRD["type"]
                rslt_tuple.append((onep,method_name,classif_count,classif_name,classif_id,classif_nb_rd_related,group_name,group_id,group_count,
                                rd_name,rd_id,rd_type,rank,is_rdi))
            # else:
            #     print(f"This group {group_id} have only one rd match ")
    return rslt_tuple
    


##################################################################################################################################
t0 = time.perf_counter()

os.makedirs(PATH_OUTPUT_COMPARE_METRIC_CLASSIF, exist_ok=True)
os.makedirs(PATH_OUTPUT_COMPARE_METRIC_CLASSIF + "/xlsx/", exist_ok=True)



#########################################################################
# # Set up argument parsing
# parser = argparse.ArgumentParser(description="Process inputs for the script.")

# # Arguments for file paths and file names
# parser.add_argument('--user_nb_top_rd', type=int, required=True)
# parser.add_argument('--onep', type=str, required=True)


# # Parse the arguments
# args = parser.parse_args()

# user_nb_top_rd = args.user_nb_top_rd  
# onep = args.onep 
#########################################################################

user_nb_top_rd = 50
onep = "P0001068"

#########################################################################
print(f"\n\n############################################")
print(f"\n\n############################################")
print(f"{onep} : START  5_metric_classif_per_patient limite to  the top {user_nb_top_rd}")

print(f"{onep} : START  5_metric_classif_per_patient limite to  the top {user_nb_top_rd}")

print(f"{onep} : get the classification of the top {onep} RDs for the {onep}")

#################################################################


## Load classif preferentiel parent (pd 7) and type (pd1)
df_pd1 = pd.read_excel(PATH_OUTPUT_DF_PRODUCT1,index_col=0,engine='openpyxl')
# df_pd7 = pd.read_excel(PATH_OUTPUT_DF_PRODUCT7,index_col=0)
df_classif = pd.read_excel(PATH_OUTPUT_DF_PC_CLASSIF,index_col = 0)
 

## Get file from product (for classification)
pd_orphanet_classif = os.listdir(PATH_OUTPUT_PRODUCT_CLASSIF)
pd_orphanet_classif_xlsx = []
for one in pd_orphanet_classif:
    if ".xlsx" in one:
        pd_orphanet_classif_xlsx.append(one)

# Get ranking RDI for the given patient
#df_init_g = df_compare_methode_global[df_compare_methode_global['patient'] == onep]
df_init_g = pd.read_excel(PATH_OUTPUT_COMPARE_RSLT_PER_PATIENT + "/" + onep+".xlsx",index_col=0,sheet_name="RDI")


try:
    rdi = df_init_g["ORPHAcode"].values[0]
except IndexError:
    rdi = ""


rdi_name,rdi_type = get_name_rype_pd1(df_pd1,rdi)
if rdi in df_classif['child_id'].tolist():
    list_classif = set(df_classif[df_classif['child_id']== rdi]["root_name"] )
    print(f"{onep} - Top {user_nb_top_rd} : {rdi} classif available in the col parent")
elif rdi in df_classif['parent_id'].tolist():
    list_classif = set(df_classif[df_classif['child_id']== rdi]["root_name"] )
    print(f"{onep} - Top {user_nb_top_rd} : {rdi} classif available in the col child")



variables = ["nb_hpo_terms", "nb_hpo_categorie", "mean_depth", "semantic_variability", "mean_IC", "proportion_general_terms"]


# Create the result dictionary
result_dict = {}
result_dict["patient"] = {"id": onep}

result_dict["rdi"] = {"id": rdi, 
                      "Name": rdi_name,
                      "Type":rdi_type,
                      "classif":list(list_classif)
                      }

 


try:
    get_classif_rdi = result_dict["rdi"]['classif']
    print(f"{onep} : The RDI {rdi} belong to {len(get_classif_rdi)}  classification")
    #################################################################

    ## 2. now let get the top 10 RD of each methods and its classif pp

    ## STEP  
    df_step = pd.read_excel(PATH_OUTPUT_COMPARE_RSLT_PER_PATIENT + "/" + onep+".xlsx",index_col=0,sheet_name="RSD")
    df_step = df_step[df_step['rank'].isin([*range(1,user_nb_top_rd+1)])].reset_index().sort_values(by='rank')

    list_rd_step = df_step['ORPHAcode'].tolist()
    # wxrking without the pp make the class go from 1 to more than 1 
    ## Before with the preferential parent
    # df_pd7[df_pd7['ORPHACode'].isin(list_rd_step)]['Classif_name'].drop_duplicates().tolist()
    # add the rdi in case it not in the top n required 
    if rdi not in list_rd_step:
        list_rd_step.append(rdi)
        print(f'{onep} RSD : RDI : {rdi} added')
    get_classif_step =     df_classif[(df_classif['parent_id'].isin(list_rd_step)) | (df_classif['child_id'].isin(list_rd_step))]['root_name'].drop_duplicates()

    result_dict = get_related_group_pp_json(result_dict,"RSD",df_init_g["RSD"].values[0],get_classif_step,list_rd_step,pd_orphanet_classif_xlsx)
    print(f"{onep} : RSD : The top {user_nb_top_rd } RDs belong to {len(get_classif_step)} classification ")
    #################################################################

    ## SM
    df_sm = pd.read_excel(PATH_OUTPUT_COMPARE_RSLT_PER_PATIENT + "/" + onep+".xlsx",index_col=0,sheet_name="RA")
    df_sm = df_sm[df_sm['rank'].isin([*range(1,user_nb_top_rd+1)])].reset_index().sort_values(by='rank')

    list_rd_sm = df_sm['ORPHAcode'].tolist()
    if rdi not in list_rd_sm:
        list_rd_sm.append(rdi)
        print(f'{onep} RA : RDI {rdi} added')
    get_classif_sm = df_classif[(df_classif['parent_id'].isin(list_rd_sm)) | (df_classif['child_id'].isin(list_rd_sm))]['root_name'].drop_duplicates()

    result_dict = get_related_group_pp_json(result_dict,"RA",df_init_g["RA"].values[0],get_classif_sm,list_rd_sm,pd_orphanet_classif_xlsx)
    print(f"{onep} : RA : The top {user_nb_top_rd }  RDs belong to {len(get_classif_sm)}  classification")
    #################################################################

    ## RW
    df_pg = pd.read_excel(PATH_OUTPUT_COMPARE_RSLT_PER_PATIENT + "/" + onep+".xlsx",index_col=0,sheet_name="RARW")
    df_pg = df_pg[df_pg['rank'].isin([*range(1,user_nb_top_rd+1)])].reset_index().sort_values(by='rank_sum_degres_pg')

    # Get hubs
    # df_smdpg_top10 = df_pg[df_pg['rank_sum_degres_pg'].isin([*range(1,user_nb_top_rd+1)])].reset_index().sort_values(by='rank_sum_degres_pg')
    list_rd_pg = df_pg['ORPHAcode'].tolist()
    if rdi not in list_rd_pg:
        list_rd_pg.append(rdi)
        print(f'{onep} RARW :RDI: {rdi} added')

    get_classif_rarw = df_classif[(df_classif['parent_id'].isin(list_rd_pg)) | (df_classif['child_id'].isin(list_rd_pg))]['root_name'].drop_duplicates()

    result_dict = get_related_group_pp_json(result_dict,"RARW",df_init_g["RARW"].values[0],get_classif_rarw,list_rd_pg,pd_orphanet_classif_xlsx)
    print(f"{onep}: RARW : The top {user_nb_top_rd } RDs belong to {len(get_classif_rarw)} classification")
    #################################################################


    ### build df to make fig
    rslt_tuple = []
    rslt_tuple = from_json_to_df_classif(df_step,onep,rdi,result_dict,"RSD",rslt_tuple)
    rslt_tuple = from_json_to_df_classif(df_sm,onep,rdi,result_dict,"RA",rslt_tuple)
    rslt_tuple = from_json_to_df_classif(df_pg,onep,rdi,result_dict,"RARW",rslt_tuple)
    df_classif_grp_rd = pd.DataFrame(rslt_tuple,columns=["type","method","nb_classif_pp","classif_name","classif_id","group_count","group_name","group_id","rd_count","rd_name","rd_id","rd_type","rank",'is_rdi'])




    with pd.ExcelWriter(PATH_OUTPUT_COMPARE_METRIC_CLASSIF + "/xlsx/" + onep +".xlsx") as writer:  
        df_classif_grp_rd.to_excel(writer,sheet_name='classif') 
    

    print(f"{onep}: Export json and xlsx")

except IndexError:
    print(f'{onep}: /!\ No info for  the {onep} ')
    print(f'{onep}: /!\ No info for  the {onep} ')


print(f"{onep}: END  5_metric_classif_per_patient done in {time.perf_counter() - t0:.1f}s")
print(f"{onep}: END  5_metric_classif_per_patient done in {time.perf_counter() - t0:.1f}s")

#################################################################



 