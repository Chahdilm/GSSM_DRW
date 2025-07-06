from set_log import * 
from classes.sim_measure_cal import Sim_measure
from path_variable import (
    PATH_OUTPUT_DF_PRODUCT4_MATCH_RSD,
    PATH_OUTPUT_MM,
    PATH_OUTPUT_DF_PRODUCT4_MATCH_RSD,
)
from sim_common import (add_common_args,parse_vector_weights,make_output_dir)


def lauch_sm_mm():
    args = add_common_args()
    print(f"Parameters: {args}")

    # 1. Parse weights & prepare output directory
    weights = parse_vector_weights(args.vector_str)
    out_dir = make_output_dir(PATH_OUTPUT_MM,args.combine,args.method,args.is_freq,
        args.pd4,args.vector_str)

    # 2. Load dataframes
    df_raredisease_2 = pd.read_excel(PATH_OUTPUT_DF_PRODUCT4_MATCH_RSD,index_col =0) 
    rd_id_list_2 = df_raredisease_2['ORPHAcode'].drop_duplicates().tolist()

    df_raredisease = pd.read_excel(PATH_OUTPUT_DF_PRODUCT4_MATCH_RSD,index_col =0) 
    # df_raredisease = df_raredisease[df_raredisease['ORPHAcode'] ==" ORPHA:610"]  # 610   166024
    rd_id_list = df_raredisease['ORPHAcode'].drop_duplicates().tolist()

 
    # 4. Initialize similarity engine
    sim = Sim_measure(df_raredisease_2,df_raredisease,"ORPHAcode","ORPHAcode")

    # 5. Run (or export empty if RD not in dataset)
    if args.param_rd not in df_raredisease_2["ORPHAcode"].tolist():
        empty_df = pd.DataFrame(columns=["RDs", "patients", "score"], index=[0])
        empty_path = f"{out_dir}/{args.index}_{args.param_rd.replace(':','-')}.xlsx"
        sim.export_sm(empty_df, empty_path)
        print(f"RD {args.param_rd} not in dataset; exported empty to {empty_path}")
    else:
        sim.compute_sm(
            args.index,
            args.param_rd,
            rd_id_list_2,
            args.combine,
            args.method,
            args.is_freq,
            weights,
            out_dir
        )



if __name__ == "__main__":
    lauch_sm_mm()