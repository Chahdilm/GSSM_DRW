
from set_log import * 
from path_variable import COL_DF_PRODUCT4_ORPHACODE


class PostLauch:
    def build_yaml_rds(self,df_rd,output_path):
        """
        Extract and dedupe ORPHA codes from the given DataFrame,
        build a Snakemake config dict, write it to YAML, and return it.
        """
        raw_codes = df_rd[COL_DF_PRODUCT4_ORPHACODE].dropna().astype(str)
        rds = {code.strip() for code in raw_codes
               if code.strip().startswith("ORPHA")}

        config_data = {
            "n": len(rds),
            "param_RD": {i+1: code for i, code in enumerate(sorted(rds))}
        }

        with open(output_path, "w") as f:
            yaml.dump(config_data, f, default_flow_style=False)

        return config_data
