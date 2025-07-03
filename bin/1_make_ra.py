from set_log import * 
from classes.sim_measure_cal import Sim_measure
from path_variable import (
    PATH_OUTPUT_DF_PATIENT_ONLY_DISORDER_WITH_ONTOLOGYX,
    PATH_OUTPUT_SM,
    PATH_OUTPUT_DF_PRODUCT4_MATCH_RSD,
)
from sim_common import (add_common_args,parse_vector_weights,make_output_dir)
 
def run_for_rd(sim,index,rd,patients,patients_rds,combine,method,is_freq,weights,out_dir):
    """Compute SM table and CDF (if applicable), export both as Excel."""
    rd_file = rd.replace(":", "-")
    df_sm = sim.run_sm_freq(rd, patients, combine, method, is_freq, weights)

    sm_path =  f"{out_dir}/{index}_{rd_file}.xlsx"
    sim.export_sm(df_sm, sm_path)
    print("Exported SM to %s", sm_path)

    # CDF only if this RD occurs in patient list
    if rd in patients_rds:
        df_cdf = sim.from_sm_make_cdf(df_sm,"Disease")
    else:
        df_cdf = pd.DataFrame(columns=["patients","RDs"], index=[0])

    cdf_path =  f"{out_dir}/CDF_{index}_{rd_file}.xlsx"
    sim.export_sm(df_cdf, cdf_path)
    print("Exported CDF to %s", cdf_path)

def lauch_mp():
    args = add_common_args()

    print("Parameters: %s", args)

    # prepare
    weights     = parse_vector_weights(args.vector_str)
    out_dir     = make_output_dir(PATH_OUTPUT_SM,args.combine, args.method, args.is_freq, args.pd4, args.vector_str)
 
    df_patient = pd.read_excel(PATH_OUTPUT_DF_PATIENT_ONLY_DISORDER_WITH_ONTOLOGYX, index_col=0    )
    df_raredisease  = pd.read_excel(PATH_OUTPUT_DF_PRODUCT4_MATCH_RSD, index_col=0    )

    patients_ids = df_patient["phenopacket"].drop_duplicates().tolist()
    patients_rds = set(df_patient["Disease"].drop_duplicates().tolist())

    sim = Sim_measure(
        df_patient, df_raredisease,"phenopacket", "ORPHAcode"  )

    if args.param_rd not in df_raredisease["ORPHAcode"].tolist():
        # no matches → export empty
        print("RD %s not in dataset; exporting empty result", args.param_rd)
        sim.export_sm(
            pd.DataFrame(columns=["RDs","patients","score"], index=[0]),
              f"{out_dir}/{args.index}_{args.param_rd.replace(':','-')}.xlsx"
        )
    else:
        run_for_rd(
            sim, args.index, args.param_rd, patients_ids, patients_rds,
            args.combine, args.method, args.is_freq, weights, out_dir
        )

if __name__ == "__main__":
    lauch_mp()