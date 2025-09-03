import os
import argparse




# output directory helper
def make_output_dir(base, combine, method,is_freq, pd4, vector_str):
    out =  f"{base}/{combine}/{method}/{is_freq}/{pd4}/{vector_str}"
    os.makedirs(out,exist_ok=True)
    return out

# weight parser
def parse_vector_weights(vector_str: str):
    return [float(x) for x in vector_str.split("_")]

 

###########################################
### SNAKEFILE
# include RSd config vector
def generate_weight_vec():
    weight_vec = []
    for v4 in range(0, 2):            # v4 ∈ {0,1}
        for v3 in range(v4, v4 + 2):  # v3 ≥ v4 and v3 − v4 ≤ 1
            for v2 in range(v3, v3 + 2):
                for v1 in range(v2, v2 + 2):
                    for v0 in range(v1, v1 + 2):
                        if v0 >= 1:
                            weight_vec.append(f"{v0}_{v1}_{v2}_{v3}_{v4}")
    # weight_vec.append('0.99_0.77_0.65_0.63_0.94')
    # weight_vec.append('2.74_5.21_9.96_12.36_3.07')
    # weight_vec.append('0.98_0.18_0.01_0_0.77')
    # weight_vec.append('0.01_0.60_0.92_1_0.15')
    # weight_vec.append('5.16_0.90_0.46_0.39_2.54')
    # weight_vec.append('5_3_2_1_4')
    # weight_vec.append('5_2_1_1_3')
    # weight_vec.append('1.2_0.9_0.7_0.6_1')
    # weight_vec.append('1_1_0_1_0')
    return weight_vec




# Build expected files
def build_base_dirs(base_path,params_RD_dict,n,combine,sm_method,selected_vectors,weight_flag,product4):
    for i in range(1, n+1):
        param = params_RD_dict[i]
        param_file = param.replace(":", "-")
        for cmb in combine:
            for sm in sm_method:
                for vw in selected_vectors:
                    # coerce all parts to strings
                    base_dir = os.path.join(
                        str(base_path),
                        str(cmb),
                        str(sm),
                        str(weight_flag),
                        str(product4),
                        str(vw)
                    )
                    yield i, param_file, cmb, sm, vw, base_dir


def select_vectors(workflow_cfg, vector_strs, n_weights):
    """
    workflow_cfg: dict, vector_strs: list[str], n_weights: int) -> list[str]
    Returns either the full list of vector_strs or a single validated vector
    passed in workflow_cfg["vector_str"] (numeric or underscore‐delimited).
    """
    vs_req = workflow_cfg.get("vector_str")
    # No override requested; use all vectors
    if vs_req is None:
        return vector_strs

    vs_raw = str(vs_req)
    # If it's purely digits and of the right length, try to reconstruct with underscores
    if vs_raw.isdigit():
        if len(vs_raw) != n_weights:
            raise ValueError(
                f"Invalid numeric vector_str '{vs_req}': "
                f"expected {n_weights} digits, got {len(vs_raw)}."
            )
        candidate = "_".join(vs_raw)
        if candidate not in vector_strs:
            raise ValueError(
                f"Invalid vector_str '{vs_req}'; reconstructed '{candidate}' "
                f"is not in allowed vectors {vector_strs}."
            )
        return [candidate]

    # Otherwise treat it as a literal underscore‐delimited string
    if vs_raw in vector_strs:
        return [vs_raw]

    raise ValueError(
        f"Invalid vector_str '{vs_req}'. Must be one of {vector_strs}, "
        "or a digit string of length {n_weights} that reconstructs to one."
    )



 