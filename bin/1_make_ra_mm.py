from bin.set_log import * 
from bin.classes.sim_measure_cal import Sim_measure
from bin.path_variable import (
    PATH_OUTPUT_DF_PRODUCT4_MATCH_RSD,
    PATH_OUTPUT_MM,
    PATH_OUTPUT_DF_PRODUCT4_MATCH_RSD,
    PATH_OUTPUT_PRODUCT, # temp a sup 
)
from bin.sim_common import (parse_vector_weights,make_output_dir)


def lauch_sm_mm(index,param_rd,combine,method,is_freq,pd4,vector_str):
 
    print(f"Parameters: {index}\t{param_rd}\t{combine}\t{method}\t{is_freq}\t{pd4}\t{vector_str}\t")

    # 1. Parse weights & prepare output directory
    weights = parse_vector_weights(vector_str)
    out_dir = make_output_dir(PATH_OUTPUT_MM,combine,method,is_freq,pd4,vector_str)

    # mini_rd = [
    #     "ORPHA:610",
    #     "ORPHA:100985",
    #     "ORPHA:412057",
    #     "ORPHA:329284",
    #     "ORPHA:100991",
    #     "ORPHA:34516",
    #     "ORPHA:79445",
    #     "ORPHA:1465",
    #     "ORPHA:99949",
    #     "ORPHA:663"
    # ]

    # 2. Load dataframes
    df_raredisease = pd.read_excel(PATH_OUTPUT_DF_PRODUCT4_MATCH_RSD,index_col =0) 
    rd_id_list = df_raredisease['ORPHAcode'].drop_duplicates().tolist()
    df_raredisease = df_raredisease[df_raredisease['ORPHAcode'].isin(rd_id_list)]  # 610   166024

 
    df_raredisease_2 = pd.read_excel(PATH_OUTPUT_DF_PRODUCT4_MATCH_RSD,index_col =0) 
    df_raredisease_2 = df_raredisease_2[df_raredisease_2['ORPHAcode'].isin(rd_id_list)]  # 610   166024


    # 4. Initialize similarity engine
    sim = Sim_measure(df_raredisease_2,df_raredisease,"ORPHAcode","ORPHAcode")

    # 5. Run (or export empty if RD not in dataset)
    if param_rd not in df_raredisease_2["ORPHAcode"].tolist():
        empty_df = pd.DataFrame(columns=["RDs", "patients", "score"], index=[0])
        empty_path = f"{out_dir}/{index}_{param_rd.replace(':','-')}.xlsx"
        sim.export_sm(empty_df, empty_path)
        print(f"RD {param_rd} not in dataset; exported empty to {empty_path}")
    else:
        sim.compute_sm(
            index,
            param_rd,
            rd_id_list,
            combine,
            method,
            is_freq,
            weights,
            out_dir
        )



if __name__ == "__main__":
    # #########################################################################
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Process inputs for the script.")

    # # Arguments 
    parser.add_argument("index", help="Run identifier")
    parser.add_argument("param_rd", help="Target ORPHA code, e.g. ORPHA:610")
    parser.add_argument("combine", choices=["funSimMax", "funSimAvg", "BMA", 'rsd'])
    parser.add_argument("method", choices=["resnik", "lin", "jiang"])
    parser.add_argument("is_freq", choices=["y", "n"])
    parser.add_argument("pd4", help="Product4 dataset label")
    parser.add_argument("vector_str", help="Weights e.g. '0.99_0.77_0.65'")

    # # Parse the arguments
    args = parser.parse_args()

    index = args.index  
    param_rd = args.param_rd  
    combine = args.combine  
    method = args.method  
    is_freq = args.is_freq  
    pd4 = args.pd4  
    vector_str = args.vector_str  
    ########################################################################
    # ## Load RD mapping
    # with open(PATH_OUTPUT_PRODUCT+"/RDs_all.yaml", "r") as f:
    #     rd_config = yaml.safe_load(f)

    # index = 1  
    # param_rd =rd_config["param_RD"]
    # combine = "funSimMax"
    # method = "resnik"
    # is_freq = "n"
    # pd4 = "productmai2024_all_vectors_withontologyX"
    # vector_str = "1_1_1_1_1"  #'3_2_2_2_1'
    
    # for onerd in param_rd.values():
    #     lauch_sm_mm(index,onerd,combine,method,is_freq,pd4,vector_str)

    lauch_sm_mm(index,param_rd,combine,method,is_freq,pd4,vector_str)