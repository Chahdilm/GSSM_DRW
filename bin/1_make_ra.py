from bin.set_log import * 
from bin.classes.sim_measure_cal import Sim_measure
from bin.path_variable import (
    PATH_OUTPUT_DF_PATIENT_ONLY_DISORDER,
    PATH_OUTPUT_SM,
    PATH_OUTPUT_DF_PRODUCT4_MATCH_RSD,
    COL_DF_PATIENT_PATIENT,
    COL_DF_PATIENT_ORPHACODE,
    PATH_YAML_PRODUCT4,
    COL_DF_PRODUCT4_ORPHACODE,
)
from bin.sim_common import (parse_vector_weights,make_output_dir)

from bin.classes.dataset import DataSet


def lauch_sm_mp(df_p,df_m,vector_str,combine,method,is_freq,pd4,param_rd,index):

    # prepare
    weights     = parse_vector_weights(vector_str)
    out_dir     = make_output_dir(PATH_OUTPUT_SM, combine,method ,is_freq ,pd4  , vector_str)


    patients_ids = df_p[COL_DF_PATIENT_PATIENT].drop_duplicates().tolist()
    patients_rds = set(df_p[COL_DF_PATIENT_ORPHACODE].drop_duplicates().tolist())

    sim = Sim_measure(df_p, df_m,COL_DF_PATIENT_PATIENT, "ORPHAcode"  )

    if param_rd not in df_m["ORPHAcode"].tolist():
        # no matches → export empty
        empty_df = pd.DataFrame(columns=["RDs", "patients", "score"], index=[0])
        empty_path = f"{out_dir}/{args.index}_{param_rd.replace(':','-')}.xlsx"

        print("RD %s not in dataset; exporting empty result", param_rd)
        sim.export_sm(empty_df,empty_path)
    else:
        sim.compute_sm_cdf(index,param_rd, patients_ids, patients_rds,
           combine,method,is_freq, weights, out_dir
        )

if __name__ == "__main__":
    ########################################################################
    # index = 1  
    # param_rd =rd_config["param_RD"]
    # combine = "funSimMax"
    # method = "resnik"
    # is_freq = "n"
    # pd4 = "productmai2024_all_vectors_withontologyX"
    # vector_str = "1_1_1_1_1"  #'3_2_2_2_1'

    ########################################################################
    # Parse the arguments
    parser = argparse.ArgumentParser(description="Process inputs for the script.")

    ## Arguments 
    parser.add_argument("index", help="Run identifier")
    parser.add_argument("param_rd", help="Target ORPHA code, e.g. ORPHA:610")
    parser.add_argument("combine", choices=["funSimMax", "funSimAvg", "BMA", 'rsd'])
    parser.add_argument("method", choices=["resnik", "lin", "jiang"])
    parser.add_argument("is_freq", choices=["y", "n"])
    parser.add_argument("pd4", help="Product4 dataset label")
    parser.add_argument("vector_str", help="Weights e.g. '0.99_0.77_0.65'")
    ## Parse the arguments    
    args = parser.parse_args()
    print("Parameters: %s", args)

    vector_str =args.vector_str
    combine =args.combine
    method =args.method
    is_freq =args.is_freq
    pd4 =args.pd4
    param_rd =args.param_rd
    index = args.index  
    ########################################################################

    df_patient = pd.read_excel(PATH_OUTPUT_DF_PATIENT_ONLY_DISORDER, index_col=0    )
    df_patient = df_patient[df_patient[COL_DF_PATIENT_PATIENT] == "P0001068"]
    df_raredisease  = pd.read_excel(PATH_OUTPUT_DF_PRODUCT4_MATCH_RSD, index_col=0    )
    df_raredisease = df_raredisease[df_raredisease['ORPHAcode'] == "ORPHA:98897"]

    # 3. config yaml depending on RDs available
    print(f'Create the yaml file for the snakefile (mp/mm) process ')
    dataset= DataSet(PATH_YAML_PRODUCT4, "")
    config_yaml = dataset.build_yaml_rds(df_raredisease,COL_DF_PRODUCT4_ORPHACODE)
    with open(PATH_YAML_PRODUCT4, "w") as f:
        yaml.dump(config_yaml, f, default_flow_style=False)
    print(f"yaml file saved to {PATH_YAML_PRODUCT4}")


    lauch_sm_mp(df_patient,df_raredisease,vector_str,combine,method,is_freq,pd4,param_rd,index)

 