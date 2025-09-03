

from bin.set_log import * 
from bin.path_variable import PATH_OUTPUT_SM, PATH_OUTPUT_MM
from bin.classes.concat_sm import ConcatSm

def concat_sm():
    p = argparse.ArgumentParser(description="MM/SM processing toolkit")
    sub = p.add_subparsers(dest="command", required=True)

    # script1: concat_matrix
    mm = sub.add_parser("concat_matrix", help="Pivot & concatenate MM score matrices")
    mm.add_argument("-v", "--vector_str", required=True, dest="vector_str",
                    help="vector_str (e.g. 2_2_1_1)")
    mm.add_argument("--col1", required=True, help="name of first pivot column")
    mm.add_argument("--col2", required=True, help="name of second pivot column")
    mm.add_argument("--pdtype_pattern", default="productmai2024_all_vectors_withontologyX",
                    help="pattern to identify PD type in path")

    # script2: process_similarity
    sm = sub.add_parser("process_similarity", help="Concat & rank SM/CDF outputs")
    sm.add_argument("-v", "--vector_str", required=True, dest="vector_str",
                    help="vector_str (e.g. 1_1_1_1_1)")
    sm.add_argument("--col1", required=True, help="name of sample column (e.g. patients)")
    sm.add_argument("--col2", required=True, help="name of label column (e.g. RDs)")
    sm.add_argument("--pdtype_pattern", default="productmai2024_controvector_withontologyX",
                    help="pattern to identify PD type in path")


    args = p.parse_args()



    concatSm = ConcatSm(args.vector_str,args.col1,args.col2)

    if args.command == "concat_matrix":
        concatSm.concat_matrix(PATH_OUTPUT_MM )
    else:  # process_similarity
        concatSm.process_similarity(PATH_OUTPUT_SM,args.pdtype_pattern )


if __name__ == "__main__":
    concat_sm()



