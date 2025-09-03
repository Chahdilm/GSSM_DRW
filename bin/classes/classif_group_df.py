from bin.path_variable import (PATH_OUTPUT_PRODUCT_CLASSIF)
from bin.set_log import * 
import re 

type_to_keep = [
 'Category',
 'Clinical group',
]

interaction_pp = set()

## Get file from product (for classification)
pd_orphanet_classif = os.listdir(PATH_OUTPUT_PRODUCT_CLASSIF)
for excel_file in pd_orphanet_classif:
    if ".xlsx" in excel_file:
        print(excel_file)
        #pd_orphanet_classif_xlsx.append(one)
        # Collect unique interactions as tuples: (rd, related_group)

        # Load the classification DataFrame for this motif.

        # df_pd_classif = pd.read_excel(os.path.join(PATH_OUTPUT_PRODUCT_CLASSIF, excel_file), index_col=0)
        df_pd_classif = pd.read_excel(os.path.join("/home/maroua/Bureau/my_pipeline_v3/GSSM_DRW/output/pd_orphanet/Classifications/ORPHAclassification_181_rare_neurological_diseases_en_2024.xlsx"), index_col=0)
        if len(df_pd_classif) != 0:
            #  regex to substitute the unwanted parts
            classif_name = re.sub(r'^ORPHAclassification_\d+_(.*?)_en_2024\.xlsx$', r'\1', excel_file)

            df_pd_classif[ df_pd_classif["child_id"] == "ORPHA:610" ] 
            ## get the parents of rdi
            group_n1 = df_pd_classif[ df_pd_classif["child_id"] == "ORPHA:610" ]['parent_id'].unique()
            



            # For the pp, get related groups from both the child and parent positions.
            root_id = df_pd_classif['root'].values[0]
            root_name = df_pd_classif['root_name'].values[0]
            for parent_from_root in df_pd_classif["parent_id"].tolist():            
                type_parent_root = df_pd_classif[df_pd_classif['parent_id'] == parent_from_root]['parent_type'].drop_duplicates().values[0]
                ## keep only group 
                if type_parent_root  in type_to_keep:
                    interaction_pp.add((classif_name,root_id,root_name,parent_from_root,type_parent_root))

            for child_from_root in df_pd_classif["child_id"].tolist():
                type_child_root = df_pd_classif[df_pd_classif['child_id'] == child_from_root]['child_type'].drop_duplicates().values[0]
                ## keep only group 
                if type_child_root  in type_to_keep:
                    interaction_pp.add((classif_name,root_id,root_name,child_from_root,type_child_root))

df_clasif_only_group = pd.DataFrame(interaction_pp, columns=['classif_name','root_group_id','root_group_name','group_id',"group_name"])

df_clasif_only_group.to_excel(PATH_OUTPUT_PRODUCT + "/classif_only_group.xlsx")

###########################################################################################################################


df_list = []
## Get file from product (for classification)
pd_orphanet_classif = os.listdir(PATH_OUTPUT_PRODUCT_CLASSIF)
for excel_file in pd_orphanet_classif:
    if ".xlsx" in excel_file:
        print(excel_file)

        # Load the classification DataFrame for this motif.
        df_pd_classif = pd.read_excel(os.path.join(PATH_OUTPUT_PRODUCT_CLASSIF, excel_file), index_col=0)
        if len(df_pd_classif) != 0:
            df_list.append(df_pd_classif)

df_all_clasiff = pd.concat(df_list)

df_all_clasiff.to_excel(PATH_OUTPUT_PRODUCT + "/classifs.xlsx")
















## Get direct parents of the rdi 
rdi = 'ORPHA:610'
rdi_pp = df_pd7[df_pd7['ORPHACode'].isin(rdi_ids)]["Classif_id"].values[0]

df_pd_classif_f_pp = df_pd_classif[df_pd_classif["root"] == (rdi_pp)]
direct_parents = df_pd_classif_f_pp[df_pd_classif_f_pp['child_id'] == rdi]
direct_parents_list = direct_parents['parent_id'].drop_duplicates().tolist()

# Step 2: Traverse hierarchy separately for each direct parent
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

len(hierarchies['ORPHA:206644'])
## prendre le n+2
for key,list_parent in hierarchies.items():
    if key == "ORPHA:206644":
        for el in list_parent:
            if el[2] <= 2:
                print(el)
 

"""
while current_ids:
    next_ids = []
    for cid in current_ids:
        # it means that the node is already visited
        if cid in visited:
            continue
        visited.add(cid)
        # Get rows where the child is this cid
        rows = df_pd_classif[df_pd_classif['child_id'] == cid]
        group_n1 = rows['parent_id'].drop_duplicates().tolist()
        for onep in group_n1:

            parent_id = rows['parent_id'].values[0]
            parent_type = rows['parent_type'].values[0]
            hierarchy.append((parent_id, parent_type))
            next_ids.append(parent_id)  # Traverse up
    current_ids = next_ids

"""