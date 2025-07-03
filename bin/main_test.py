
from classes.post_lauch import PostLauch
from classes.dataset import DataSet
from set_log import * 
from path_variable import (
    PATH_OUTPUT_DF_PRODUCT4_MATCH_RSD,
    PATH_OUTPUT_DF_PRODUCT4,
    PATH_INPUT,
    PATH_INPUT_PRODUCT4_XML,
    PATH_OUTPUT_PRODUCT4_JSON,
    PATH_YAML_PRODUCT4
)
def load_or_build_dataframe():
    """Load the cached DF or build it from scratch."""
    if os.path.exists(PATH_OUTPUT_DF_PRODUCT4_MATCH_RSD):
        df = pd.read_excel(PATH_OUTPUT_DF_PRODUCT4_MATCH_RSD, index_col=0)
        print(f"Loaded cached DataFrame…")
        return df

    # else: build from XML → JSON → DataFram
    print(f"Created new DataFrame")
    # json file product 4
    build_json = DataSet(PATH_INPUT_PRODUCT4_XML, "")
    json_rd = build_json.from_xml_to_json()
    build_json.save_json(PATH_OUTPUT_PRODUCT4_JSON, json_rd)
    # df file product 4
    build_df = DataSet(PATH_OUTPUT_PRODUCT4_JSON, "")
    df = build_df.build_orpha_df()
    df.to_excel(PATH_OUTPUT_DF_PRODUCT4)

    # filter based on orphacode list from RSD list
    with open(PATH_INPUT + "/orphacode_rsd.txt") as f:
        rsd_list = {"ORPHA:" + line.strip() for line in f}
    all_orpha = set(df["ORPHAcode"])
    match = all_orpha & rsd_list
    ## get match RDs between product4 and rsd only
    df_filt = df[df["ORPHAcode"].isin(match)]
    df_filt.to_excel(PATH_OUTPUT_DF_PRODUCT4_MATCH_RSD)
    
    print(f'nb RD rsd {len(df_filt['ORPHAcode'].drop_duplicates())}, frequency available {set(df_filt['hpo_frequency'])}')

    return df_filt


if __name__ == "__main__":
    df_rd = load_or_build_dataframe()

    print(f'Create the yaml file for the snakefile (mp/mm) process ')
    postl= PostLauch()
    config_yaml = postl.build_yaml_rds(df_rd,PATH_YAML_PRODUCT4)

 
