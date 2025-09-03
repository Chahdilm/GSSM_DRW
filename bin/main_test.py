
from bin.classes.dataset import DataSet
from bin.set_log import * 
from bin.path_variable import *


def convert_and_build_dataframe(path_xml,path_json,nb_type):
    """Load the cached DF or build it from scratch."""

    # else: build from XML → JSON → DataFram
    print(f"Created new DataFrame")
    # from xml to json
    build_json = DataSet(path_xml, "")
    json_rd = build_json.from_xml_to_json()
    build_json.save_json(path_json, json_rd)
    # from json to xlsx
    build_df = DataSet(path_json, "")
    if nb_type == 4:
        df = build_df.build_orpha_df()
    elif nb_type == 44:
        df = build_df.from_rsd_build_orpha_df()
    elif nb_type == 6:  
        df = build_df.df_pd6()
    elif nb_type == 1:
        df = build_df.df_pd1()
    elif nb_type == 7:
        df = build_df.df_pd7()
    else:
        print(f"Error: nb_type {nb_type} not recognized")
        exit()
    return df

## only for pd4 
def match_rsd(df,path_match_rsd):
    """ Filter the dataframe to keep only RDs that are also in the RSD list."""
    if os.path.exists(path_match_rsd):
        df = pd.read_excel(path_match_rsd, index_col=0)
        print(f"Loaded  DataFrame pd4 match RSD")
        return df
    else:
        ## filter based on orphacode list from RSD list
        with open(PATH_INPUT + "/orphacode_rsd.txt") as f:
            rsd_list = {"ORPHA:" + line.strip() for line in f}
        all_orpha = set(df["ORPHAcode"])
        match = all_orpha & rsd_list
        ## get match RDs between product4 and rsd only
        df_filt = df[df["ORPHAcode"].isin(match)]
        
        print(f'nb RD rsd {len(df_filt['ORPHAcode'].drop_duplicates())}, frequency available {set(df_filt['hpo_frequency'])}')

    return df_filt

def build_classif(path_input_classif,path_output_classif):
    list_classif = os.listdir(PATH_INPUT_PRODUCTCLASSIF_XML)
    for onec in list_classif:
        motif = onec.split(".")[0]
        #motif = "ORPHAclassification_150_rare_inborn_errors_of_metabolism_en_2024"
        # ORPHAclassification_150_rare_inborn_errors_of_metabolism_en_2024
        # ORPHAclassification_147_rare_developmental_anomalies_during_embryogenesis_en_2024
        # ORPHAclassification_181_rare_neurological_diseases_en_2024

        
        build_rds_json = DataSet(path_input_classif + "/"+ motif+ ".xml","")
        json_rd = build_rds_json.from_xml_to_json()
        build_rds_json.save_json(path_output_classif + "/"+ motif+ ".json", json_rd) 

        build_raredisease = DataSet(path_output_classif + "/"+ motif+ ".json","")
        df_pd_classif = build_raredisease.df_classif()
        df_pd_classif.to_excel(path_output_classif + "/"+ motif+ ".xlsx")

 


if __name__ == "__main__":
    ###########################################################
    ## for pd4
    df4 = convert_and_build_dataframe(PATH_INPUT_PRODUCT4_XML,PATH_OUTPUT_PRODUCT4_JSON,4)
    df4.to_excel(PATH_OUTPUT_DF_PRODUCT4)

    # df4_rsd = convert_and_build_dataframe(PATH_INPUT_PRODUCT4RSD_XML,PATH_OUTPUT_PRODUCT4_JSON_RSD,44)
    # df4_rsd.to_excel(PATH_OUTPUT_DF_PRODUCT4_RSD)
 

    df_rd_match_rsd = match_rsd(df4,PATH_OUTPUT_DF_PRODUCT4_MATCH_RSD)
    df_rd_match_rsd.to_excel(PATH_OUTPUT_DF_PRODUCT4_MATCH_RSD)

    ## for pd6
    df6 = convert_and_build_dataframe(PATH_INPUT_PRODUCT6_XML,PATH_OUTPUT_PRODUCT6_JSON,6)
    df6.to_excel(PATH_OUTPUT_DF_PRODUCT6)


    ## for pd1
    df1 = convert_and_build_dataframe(PATH_INPUT_PRODUCT1_XML,PATH_OUTPUT_PRODUCT1_JSON,1)
    df1.to_excel(PATH_OUTPUT_DF_PRODUCT1)


    ## for pd6
    df7 = convert_and_build_dataframe(PATH_INPUT_PRODUCT7_XML,PATH_OUTPUT_PRODUCT7_JSON,7)
    df7.to_excel(PATH_OUTPUT_DF_PRODUCT7)

    ###########################################################
    ## yaml file for snakefile
    print(f'Create the yaml file for the snakefile (mp/mm) process ')
    dataset= DataSet(PATH_YAML_PRODUCT4, "")
    config_yaml = dataset.build_yaml_rds(df_rd_match_rsd,COL_DF_PRODUCT4_ORPHACODE)
    with open(PATH_YAML_PRODUCT4, "w") as f:
        yaml.dump(config_yaml, f, default_flow_style=False)
    print(f"yaml file saved to {PATH_YAML_PRODUCT4}")
    ###########################################################


    ###########################################################
    ## build all the classifications df based on all xml classif files
    dataset= DataSet(PATH_OUTPUT_PRODUCT_CLASSIF, "")
    build_classif(PATH_INPUT_PRODUCTCLASSIF_XML,PATH_OUTPUT_PRODUCT_CLASSIF)
    print("Build all classifications files from xml to json to xlsx : Exported")
    # Merge all classification into one file
    df_all_clasiff = dataset.merge_all_classif(PATH_OUTPUT_PRODUCT_CLASSIF)
    df_all_clasiff.to_excel(PATH_OUTPUT_PRODUCT + "/classifs.xlsx")

