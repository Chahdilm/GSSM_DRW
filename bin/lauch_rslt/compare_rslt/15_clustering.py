

import argparse
import os
import sys
import numpy as np
import pandas as pd
 
# from sklearn.metrics import pairwise_distances
from sklearn.metrics import pairwise_distances,silhouette_score


from scipy.spatial.distance import squareform
from scipy.cluster.hierarchy import linkage, fcluster, dendrogram,cophenet


import matplotlib.pyplot as plt
###########################################
from bin.set_log import * 
import re 

from bin.path_variable import (
    CONFIG_ALPHA,
    PATH_OUTPUT_HM,
    PATH_OUTPUT_COMPARE_GLOBAL,
    PATH_OUTPUT_PRODUCT,
    PATH_OUTPUT_DF_PRODUCT7,
    PATH_OUTPUT_COMPARE_RSLT
)

def find_col(df, candidates):
    """Return the first matching column from candidates (case-insensitive)."""
    cols = {c.lower(): c for c in df.columns}
    for cand in candidates:
        if cand in df.columns:
            return cand
        if cand.lower() in cols:
            return cols[cand.lower()]
    return None



def best_cut_by_silhouette(Z, D_square, min_clusters, max_clusters):
    """Scanne hauteurs + midpoints pour maximiser la silhouette."""
    heights = np.unique(Z[:, 2])
    cand = set(heights.tolist())
    if heights.size >= 2:
        mids = (heights[:-1] + heights[1:]) / 2.0
        cand.update(mids.tolist())
    eps = 1e-9
    for h in heights:
        cand.add(max(0.0, h - eps))
        cand.add(h + eps)

    best_s, best_t, best_k, best_labs = -np.inf, None, None, None
    for t in sorted(cand):
        labs = fcluster(Z, t=t, criterion="distance")
        k = np.unique(labs).size
        if k < min_clusters or k > max_clusters:
            continue
        try:
            s = silhouette_score(D_square, labs, metric="precomputed")
        except Exception:
            continue
        if s > best_s:
            best_s, best_t, best_k, best_labs = s, t, k, labs
    return best_s, best_t, best_k, best_labs





# ======================= CONFIG ICI =======================
min_clusters = 2
max_clusters=100
hierarchy_level = 3
CONFIG_ALPHA = 0.30
# RA RARW_0.9


MIN_CLUSTER_SIZE_DISPLAY = 3   # <-- NEW: only show clusters with at least 3 patients
# =========================================================


GROUP_RDI = True  # if True, group by rdi, else by group_id_match
variable_alpha = f"RARW_{CONFIG_ALPHA}"

for variable_alpha in [f"RARW_{CONFIG_ALPHA}", f"RA"]:
    print(f" \n\n ==== {variable_alpha} ==== \n\n")
    df = pd.read_excel(f"{PATH_OUTPUT_HM}/info/hm_each_patient_{CONFIG_ALPHA}_{hierarchy_level}.xlsx",index_col=0)

    df = df[(df['method'] == variable_alpha) ]# & df['rank_rd'] <= 10]
    patient_list = df['patient'].drop_duplicates().tolist()
    patient_list = ['P0001068','P0008744'] # "ORPHA:206644" group en commun
    if GROUP_RDI :
        ## filter only keeping rdi 
        big_list_df = []
        for onep in patient_list:
            mini_df = df[df['patient'] == onep]
            rdi = mini_df['rdi'].drop_duplicates().unique()[0]
            group_id = mini_df['group_id_match'].drop_duplicates().tolist()
            minidf_filt = mini_df[mini_df['group_id_match'].isin(group_id)]
            big_list_df.append(minidf_filt)

        df = pd.concat(big_list_df, ignore_index=True)
    print(f"Nb patient : {df['patient'].nunique()}")

    ## to get the related classif of each group_id_match
    df_all_clasiff =pd.read_excel(PATH_OUTPUT_PRODUCT + "/classifs.xlsx",index_col=0)

    print(f"{len(df['classif_id'].drop_duplicates().tolist())
    } classif \n{ df['classif_id'].drop_duplicates()
    }")

    # Detect columns if not provided
    patient_col = find_col(df, ["patient"])
    group_col   = find_col(df, ["group_id_match"])
    classif_col = find_col(df, ["classif_id", "classification_id"])

    
    df_core = df[[patient_col, group_col]].drop_duplicates()
    df_core.columns = ["patient","merge_id"]

    df_classif_modified = df_all_clasiff[["root", "parent_id"]]
    df_classif_modified.columns = ["root", "merge_id"]

    ## now if group have multiple classif it is shown
    df_cored_all_classif = df_core.merge(df_classif_modified, how="inner",on="merge_id").drop_duplicates()
    ## verify if there is multiple classif for a group exemple ORPHA:94145
    # df_cored_all_classif[df_cored_all_classif['merge_id'] == "ORPHA:94145"]

    classif_col = "root"  # use root as classif_col
    group_col = "merge_id"  # use merge_id as group_col

    # get Exact-combination clusters
    df_cored_all_classif["cluster_exact"] = df_cored_all_classif[group_col].astype(str) + " | " + df_cored_all_classif[classif_col].astype(str)
    ## verify if there is multiple classif for a group exemple ORPHA:94145
    # df_cored_all_classif[(df_cored_all_classif["merge_id"] == "ORPHA:94145") & (df_cored_all_classif[patient_col] == "P0016897") ].drop_duplicates()


    ## all combo RD | classif
    combos = sorted(df_cored_all_classif["cluster_exact"].unique())
    print(f"{len(combos)} combinaison RD|classif possible, tot {len(df_cored_all_classif['cluster_exact'])}")
    ## count each combo and add an id 
    combo_to_id = {c: i + 1 for i, c in enumerate(combos)}
    df_cored_all_classif["cluster_exact_id"] = df_cored_all_classif["cluster_exact"].map(combo_to_id)

    ## # Matrice patients x features (binaire)
    # Build patient x pair presence matrix, create a new df for the asign part 
    df_pairs = df_cored_all_classif.assign(pair=df_cored_all_classif["cluster_exact"])
    X = (df_pairs
            .assign(val=1)
            .pivot_table(index=patient_col, columns="pair", values="val", aggfunc="max", fill_value=0)
            )
    patients = X.index.tolist() # or df[patient_col].drop_duplicates().tolist() same rslt



    # Distance Jaccard
    D = pairwise_distances(X.astype(bool).values, metric="jaccard") # jaccard cosine (nul : dice euclidean)
    np.fill_diagonal(D, 0.0)
    D = (D + D.T) / 2.0

    # Hierarchical clustering 
    ## Convert a vector-form distance vector to a square-form distance matrix, and vice-versa.
    Dc = squareform(D, checks=False)

    Z = linkage(Dc, method="average") # average complete
    coph_corr, _ = cophenet(Z, Dc)    

    # FIX: sélection du meilleur seuil par silhouette (et PAS avant d’avoir Z)

    best_s, best_t, best_k, best_labels = best_cut_by_silhouette(
        Z, D, min_clusters, max_clusters    )
    # Si aucune silhouette valide (ex: tout donne k=1), fallback en 1 cluster
    if best_labels is None:
        best_labels = np.ones(len(patients), dtype=int)
        best_t = 1.0
        best_s = float('nan')
        best_k = 1

    # Affectations
    labs = best_labels
    df_sim = pd.DataFrame({patient_col: patients, "cluster_sim_id": labs})

    # Merge assignments
    df_assign = (df_cored_all_classif[[patient_col, group_col, classif_col, "cluster_exact", "cluster_exact_id"]]
                    .merge(df_sim, on=patient_col, how="left")
                    .sort_values([patient_col, "cluster_exact_id"])
                    .reset_index(drop=True))
    # df_assign.to_csv(args.out, index=False)

    print(f"[{variable_alpha}] silhouette={best_s:.3f} | cophé={coph_corr:.3f} | t*={best_t:.3f} | k={len(np.unique(labs))}")
    
    # plt.figure(figsize=(12, 6))
    # dendrogram(Z, labels=[str(p) for p in patients], leaf_rotation=90)
    # plt.title("Patient clustering dendrogram ")
    # plt.xlabel("patient_id")
    # plt.ylabel("distance")
    # plt.tight_layout()
    # plt.show()
    # # plt.savefig(args.plot, dpi=150)
    # plt.close()
    # ---- collapse small clusters for display ----
    # keep only clusters with size >= MIN_CLUSTER_SIZE_DISPLAY
    _, counts = np.unique(labs, return_counts=True)
    size_by_label = dict(zip(np.unique(labs), counts))
    keep_labels = [c for c, n in size_by_label.items() if n >= MIN_CLUSTER_SIZE_DISPLAY]
    keep_mask = np.array([l in keep_labels for l in labs])

    if keep_mask.sum() >= 2:
        patients_keep = [p for p, m in zip(patients, keep_mask) if m]
        D_keep = D[np.ix_(keep_mask, keep_mask)]
        Dc_keep = squareform(D_keep, checks=False)
        Z_keep = linkage(Dc_keep, method="average", optimal_ordering=True)

        # find a sensible color threshold for the subset (optional but nicer)
        bs, bt, bk, _ = best_cut_by_silhouette(Z_keep, D_keep, min_clusters, max_clusters)
        t_plot = float(bt) if bt is not None else float(np.median(Z_keep[:, 2]))

        print(f"Displayed clusters >= {MIN_CLUSTER_SIZE_DISPLAY}: n_patients={len(patients_keep)}, "
            f"n_clusters_shown={len(keep_labels)}")

        plt.figure(figsize=(12, 6))
        dendrogram(
            Z_keep,
            labels=[str(p) for p in patients_keep],
            leaf_rotation=90,
            color_threshold=t_plot,
            above_threshold_color="#B0B0B0",
        )
        plt.axhline(t_plot, ls="--", c="red", lw=1)
        plt.title(f"Patient clustering dendrogram (≥{MIN_CLUSTER_SIZE_DISPLAY} per cluster) - {variable_alpha}")
        plt.xlabel("patient_id")
        plt.ylabel("distance")
        plt.tight_layout()
        plt.show()
        plt.close()
    else:
        # fallback: nothing large enough to show; draw the full tree
        t_plot = float(best_t) if best_t is not None else float(np.median(Z[:, 2]))
        plt.figure(figsize=(12, 6))
        dendrogram(
            Z,
            labels=[str(p) for p in patients],
            leaf_rotation=90,
            truncate_mode="lastp",   # show only the top merges
            p=30,                    # show the last 30 clusters
            show_contracted=True,    # draw triangles for contracted parts
            color_threshold=float(best_t) if best_t is not None else None,
            above_threshold_color="#B0B0B0",
        )
        plt.axhline(float(best_t) if best_t is not None else 0.0, ls="--", c="red", lw=1)
        plt.title(f"Patient clustering dendrogram - {variable_alpha}")
        plt.xlabel("patient_id")
        plt.ylabel("distance")
        plt.tight_layout()
        plt.show()
        plt.close()

    



