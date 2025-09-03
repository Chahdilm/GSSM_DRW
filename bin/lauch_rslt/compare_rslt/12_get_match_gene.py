import pandas as pd
# from bin.set_log import * 

## avec que RA on fait remonter les genes cuasatif dans le top 20 (?) arguments exemple P0022261 


print(f"START  12_get_match_group")
 
PATH_OUTPUT_COMPARE_GLOBAL = '/home/maroua/Bureau/wip/my_pipeline_v2/output//compare_rank_1_1_1_1_1_concat_matrix_0.3//global/'
df_classif = pd.read_excel(PATH_OUTPUT_COMPARE_GLOBAL + "/global_classif.xlsx",index_col=0)

df_pd6 = pd.read_excel("/home/maroua/Bureau/my_pipeline_v3/GSSM_DRW/output/pd_orphanet/en_product6.xlsx",index_col=0 )

import json
path_patient = "/home/maroua/Bureau/my_pipeline_v3/GSSM_DRW/input/patient/SolveRD_WP1_phenopackets_v2_with_ern_13301/"
#########################################
results = []  # we will append a row‐dict for every (patient,method,topN_rd_id)
n_top = 20
# iterate over each (patient,method)
for (patient, mtd), sub in df_classif.groupby(['type','method']):
    
    ## get the gene from the json file 
    with open(f"{path_patient}/{patient}_ern.json", 'r', encoding="ISO-8859-1" ) as f:
        root_json = json.load(f)
        interp = root_json['interpretations']
        for onedict in interp:
            diag = onedict['diagnosis']['genomicInterpretations']
            for one_diag in diag:
                if 'variantInterpretation' in one_diag:
                    gene_patient = one_diag['variantInterpretation']['variationDescriptor']['geneContext']['symbol']
 


    ## Find the RDI row(s)
    is_rdi_sub = sub[sub['is_rdi'] == 'y']
    if is_rdi_sub.empty:
        # no RDI marked for this (patient,method) – skip or record NaNs
        print-(f"Warning: no RDI for (patient={patient}, method={mtd})")

    RDI_rd_id   = is_rdi_sub['rd_id'].iloc[0]
    RDI_rank    = is_rdi_sub['rank'].iloc[0]



    ## Top N rd_id by rank 
    topN_rd = (
        sub[['rd_id','rank']]
        .drop_duplicates(subset=['rd_id'])
        .sort_values(by='rank', ascending=True)
        .head(n_top)['rd_id']
        .tolist()
    )

    # 3) For each rd_id in the top 10, compute a “difference score” versus the RDI’s sets.
    for candidate in topN_rd:
        succes = 0
        try:
            get_gene_rd = df_pd6[df_pd6['ORPHACode'] == candidate]['Symbol'].values[0]
        
            if gene_patient == get_gene_rd:
                succes = 1
            
        except:
            get_gene_rd = "NA"
            succes = 0

        cand_rows = sub[(sub['rd_id'] == candidate) ]['rank'].values[0]



        # record one row in our results
        results.append({
            'patient': patient,
            "gene_patient": gene_patient,
            'method': mtd,
            'RDI_rd_id': RDI_rd_id,
            'RDI_rank': RDI_rank,

            'candidate_rd_id': candidate,
            'candidate_rank': cand_rows,
            'candidate_gene': get_gene_rd,
            'gene_match': succes,
        })

# Turn our list of dicts into a DataFrame for easy viewing:
summary_df = pd.DataFrame(results)
# summary_df.to_excel(PATH_OUTPUT_COMPARE_RSLT + 'summary_df.xlsx')


 

# ─── 2) COMPUTE CLASSIFICATION AND GROUP SIMILARITY PERCENTAGES SEPARATELY ───
def compute_gene_pct(row):
    patient_gene = set(row['gene_patient'])
    cand_gene = set(row['candidate_gene'])
    if len(patient_gene) == 0:
        return 0.0
    return 100 * (len(patient_gene & cand_gene) / len(patient_gene))

summary_df['gene_similarity_pct'] = summary_df.apply(compute_gene_pct, axis=1)

######################################################### 


# ─── 2) DEFINE METHODS AND PATIENTS ───
methods = ['RSD', 'RA', 'RARW']
patients = summary_df['patient'].unique()

# ─── 3) BUILD A FUNCTION THAT RETURNS AN HTML STRING FOR ONE METHOD‐CELL ───
def build_cell_html(pat, method):
    sub = summary_df[(summary_df['patient'] == pat) & (summary_df['method'] == method)]
    if sub.empty:
        return "NaN"
    parts = []
    for _, row in sub.iterrows():
        cand_rank = row['candidate_rank']
        cand_rd = row['candidate_rd_id']
        cand_gene = row['candidate_gene']
        gene = row['gene_match'] > 0

        if gene:
            color = 'orange'
        else:
            color = None
        if color:
            # Wrap the RD in a <span> with background color
            parts.append(f"<span style='background-color:{color};padding:2px'>{cand_gene} - {cand_rd} - [{cand_rank}]</span>")
        else:
            parts.append(cand_gene)
                # Join with <br> so each RD appears on its own line
    return "<br>".join(parts)

# ─── 4) BUILD WIDE TABLE WITH ONE COLUMN PER METHOD, VALUES=HTML ⋄────────
dict_nbgroup={}
wide_html = pd.DataFrame(columns=['patient'] + methods)
for pat in patients:
    row = {'patient': pat}
    for m in methods:
        row[m] = build_cell_html(pat, m)
    
    wide_html = pd.concat([wide_html, pd.DataFrame([row])], ignore_index=True)
 
#### get the homogenity values :
rsd = 0
ra = 0
rarw=0
for key,value in dict_nbgroup.items():
    rsd =rsd + value[0]  
    ra =ra + value[1]
    rarw =rarw + value[2]
 

print(f'The total number of RDs that belong to the same medical domain  is : RSD:{rsd}, RA: {ra}, RARW: {rarw}')

result = {}                    
for k, v in dict_nbgroup.items():    
    # get the max from value dict  
    mx = max(v)               
    indices = []  
    # get the index if multiple max             
    for i, x in enumerate(v):  
        if x == mx:
            indices.append(i)
    result[k] = (mx, indices)  



 
# ─── Convert to HTML with escape=False and display ───
from IPython.display import HTML
# wide_html_ff = wide_html[wide_html['patient'] == "P0005327"]
html_str = wide_html.to_html(escape=False)
display(HTML(html_str))
 
# wide_html_ff = wide_html[wide_html['patient'].isin(set(allp).difference(patientuniq))]
# html_str = wide_html_ff.to_html(escape=False)
# display(HTML(html_str))



#########################################
