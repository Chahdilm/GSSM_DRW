from get_packages import * 
 

 
class ParseType():

    def sm_common_args(self,parser: argparse.ArgumentParser):
        parser.add_argument("index", help="Unique run identifier")
        parser.add_argument("param_rd", help="Target ORPHA code, e.g. ORPHA:610")
        parser.add_argument(
            "combine",
            help="Combine function name, e.g. 'funSimMax', 'funSimAvg', 'BMA', 'rsd'"
        )
        parser.add_argument(
            "method",
            help="Semantic measure method, e.g. 'resnik', 'lin', 'jc', 'rel', 'ic', 'graphic'"
        )
        parser.add_argument("is_freq", choices=["y","n"], help="Whether to weight by frequency")
        parser.add_argument("pd4", help="Product4 dataset label (e.g. 'all_product4_mai_2025')")
        parser.add_argument(
            "vector_str",
            help="Weights as underscore-separated floats, e.g. '0.99_0.77_0.65_0.63_0.94'"
        )
