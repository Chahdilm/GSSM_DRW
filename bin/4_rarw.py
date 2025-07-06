from set_log import * 
from classes.random_process import (RandomWalkBatch,RandomWalkAggregator)
from path_variable import (
    PATH_OUTPUT_FOLDER_RW,
    PATH_OUTPUT_FOLDER_MATRIX_ADD_PATIENT,
    PATH_CLASSIFICATION_JSON,
    PATH_OUTPUT_DF_PATIENT_ONLY_DISORDER_WITH_ONTOLOGYX
)

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Random Walk pipeline")
    sub = p.add_subparsers(dest="command", required=True)

    run_p = sub.add_parser("run")
    run_p.add_argument("--seeds", required=True,
                        help="Space-delimited list of patient IDs")
    run_p.add_argument("--alpha", required=True, type=float)
    run_p.add_argument("--matrix_subdir", required=True)

    agg_p = sub.add_parser("aggregate")
    agg_p.add_argument("--alpha", required=True, type=float)
    agg_p.add_argument("--matrix_subdir", required=True)

    args = p.parse_args()

    if args.command == "run":
        seeds = args.seeds.split()
        batch = RandomWalkBatch(seeds, args.alpha, args.matrix_subdir,PATH_OUTPUT_FOLDER_MATRIX_ADD_PATIENT,PATH_OUTPUT_FOLDER_RW,PATH_CLASSIFICATION_JSON)
        batch.run()
    else:
        df_patient = pd.read_excel(PATH_OUTPUT_DF_PATIENT_ONLY_DISORDER_WITH_ONTOLOGYX, index_col=0)

        agg = RandomWalkAggregator(args.matrix_subdir, args.alpha,df_patient,PATH_OUTPUT_FOLDER_RW)
        agg.aggregate()


 


















# PATH_OUTPUT_FOLDER_RW = path_folder_rw
# RandomWalkAggregator((self, matrix_subdir, alpha,df_patient,path_folder_rw):)


# path_integrate_p = PATH_OUTPUT_FOLDER_MATRIX_ADD_PATIENT
# path_folder_rw
# RandomWalkBatch(self, seeds, alpha, matrix_subdir,path_integrate_p,path_folder_rw)

#         PATH_CLASSIFICATION_JSON,path_classif
#             def __init__(self, seeds, alpha, matrix_subdir,path_integrate_p,path_folder_rw,self.path_classif):
