import os
from bin.config_json import CONFIG_RD, CONFIG_ALPHA

# Compose config string
CONFIG = f"{CONFIG_RD}_{CONFIG_ALPHA}"

# Path resolution
BIN_DIR = os.path.dirname(os.path.abspath(__file__))
# BIN_DIR = "/home/maroua/Bureau/mini_pipeline_test/bin"#os.path.dirname(os.path.abspath(__file__))

PROJECT_ROOT = os.path.abspath(os.path.join(BIN_DIR, ".."))  # because path_variable is in bin folder

# Output and Input roots
PATH_OUTPUT = os.path.join(PROJECT_ROOT, "output")
PATH_INPUT = os.path.join(PROJECT_ROOT, "input")
PATH_INPUT_HPO = os.path.join(PATH_INPUT, "hpo")

# Make sure main folders exist
os.makedirs(PATH_OUTPUT, exist_ok=True)
os.makedirs(PATH_INPUT, exist_ok=True)
os.makedirs(PATH_INPUT_HPO, exist_ok=True)

# Log folder
PATH_LOG = os.path.join(PATH_OUTPUT, "log")
os.makedirs(PATH_LOG, exist_ok=True)
PATH_LOG_FILE = f"{PATH_LOG}/log_{CONFIG}.log"

# Output folders
PATH_OUTPUT_SM = os.path.join(PATH_OUTPUT, "mp_sm")
os.makedirs(PATH_OUTPUT_SM, exist_ok=True)

PATH_OUTPUT_SM_CDF_FILE = f"{PATH_OUTPUT_SM}/CDF_{CONFIG}.xlsx"

PATH_OUTPUT_MM = os.path.join(PATH_OUTPUT, "mm_sm")
os.makedirs(PATH_OUTPUT_MM, exist_ok=True)

PATH_OUTPUT_FOLDER_MATRIX_ADD_PATIENT = os.path.join(PATH_OUTPUT_MM, "patient_added")
os.makedirs(PATH_OUTPUT_FOLDER_MATRIX_ADD_PATIENT, exist_ok=True)

PATH_OUTPUT_PATIENT_SOLVERD = os.path.join(PATH_OUTPUT, "patient_solverd")
os.makedirs(PATH_OUTPUT_PATIENT_SOLVERD, exist_ok=True)
PATH_OUTPUT_DF_PATIENT_ONLY_DISORDER =f"{PATH_OUTPUT_PATIENT_SOLVERD}/patient_confirmed_solverd_only_disorder_with_ontologyX.xlsx"


# Columns (keep as string constants)
COL_DF_PATIENT_PATIENT = "phenopacket"
COL_DF_PATIENT_ORPHACODE = "Disease"

# Rare random walk output
PATH_OUTPUT_FOLDER_RW = os.path.join(PATH_OUTPUT, "rarw")
os.makedirs(PATH_OUTPUT_FOLDER_RW, exist_ok=True)

# Compare results
PATH_OUTPUT_COMPARE_RSLT = os.path.join(PATH_OUTPUT, f"compare_rank_{CONFIG}")
os.makedirs(PATH_OUTPUT_COMPARE_RSLT, exist_ok=True)
PATH_OUTPUT_COMPARE_RSLT_PER_PATIENT = os.path.join(PATH_OUTPUT_COMPARE_RSLT, "metric_patient")
os.makedirs(PATH_OUTPUT_COMPARE_RSLT_PER_PATIENT, exist_ok=True)

PATH_OUTPUT_DF_COMPARE_RANK_DIRECT = f"{PATH_OUTPUT_COMPARE_RSLT}/compare_rank_method.xlsx"

PATH_OUTPUT_COMPARE_RSLT_ANALYSIS_PER_PATIENT = os.path.join(PATH_OUTPUT_COMPARE_RSLT, "analysis_per_patient")
os.makedirs(PATH_OUTPUT_COMPARE_RSLT_ANALYSIS_PER_PATIENT, exist_ok=True)
PATH_OUTPUT_COMPARE_METRIC_CLASSIF = os.path.join(PATH_OUTPUT_COMPARE_RSLT, "metric_classif")
os.makedirs(PATH_OUTPUT_COMPARE_METRIC_CLASSIF, exist_ok=True)
PATH_OUTPUT_COMPARE_GLOBAL = os.path.join(PATH_OUTPUT_COMPARE_RSLT, "global")
os.makedirs(PATH_OUTPUT_COMPARE_GLOBAL, exist_ok=True)


#### rslt hm 
PATH_OUTPUT_HM = os.path.join(PATH_OUTPUT, f"hm")
os.makedirs(PATH_OUTPUT_HM, exist_ok=True)

# Output product
PATH_OUTPUT_PRODUCT = os.path.join(PATH_OUTPUT, "pd_orphanet")
os.makedirs(PATH_OUTPUT_PRODUCT, exist_ok=True)
PATH_OUTPUT_PRODUCT_CLASSIF = os.path.join(PATH_OUTPUT_PRODUCT, "Classifications")
os.makedirs(PATH_OUTPUT_PRODUCT_CLASSIF, exist_ok=True)


PATH_OUTPUT_DF_PC_CLASSIF =f"{PATH_OUTPUT_PRODUCT}/parent_child_classif.xlsx"
PATH_OUTPUT_DF_PC =f"{PATH_OUTPUT_PRODUCT}/parent_child_noclassif.xlsx"
PATH_OUTPUT_DF_PC_CLASSIF_v2 =f"{PATH_OUTPUT_PRODUCT}/parent_child_classif_v2.xlsx"
PATH_OUTPUT_DF_PC_v2 =f"{PATH_OUTPUT_PRODUCT}/parent_child_noclassif_v2.xlsx"


PATH_OUTPUT_PRODUCT4_JSON_RSD =f"{PATH_OUTPUT_PRODUCT}/all_rsdpd4_mai_2025.json"
PATH_OUTPUT_DF_PRODUCT4_RSD =f"{PATH_OUTPUT_PRODUCT}/all_rsdpd4_mai_2025.xlsx"
PATH_OUTPUT_PRODUCT4_JSON =f"{PATH_OUTPUT_PRODUCT}/all_enpd_mai_2025.json"
PATH_OUTPUT_DF_PRODUCT4 =f"{PATH_OUTPUT_PRODUCT}/all_enpd_mai_2025.xlsx"
PATH_OUTPUT_DF_PRODUCT4_MATCH_RSD =f"{PATH_OUTPUT_PRODUCT}/all_enpd_mai_2025_same_rd_rsd_v2.xlsx"


COL_DF_PRODUCT4_ORPHACODE = 'ORPHAcode'

PATH_LIST_PRODUCT4 =f"{PATH_OUTPUT_PRODUCT}/list_rds.txt"
PATH_YAML_PRODUCT4 =f"{PATH_OUTPUT_PRODUCT}/RDs_all.yaml"
PATH_CLASSIFICATION_JSON =f"{PATH_OUTPUT_PRODUCT}/classif_orpha.json"


PATH_OUTPUT_PRODUCT7_JSON =f"{PATH_OUTPUT_PRODUCT}/en_product7.json"
PATH_OUTPUT_DF_PRODUCT7 =f"{PATH_OUTPUT_PRODUCT}/en_product7.xlsx"
PATH_OUTPUT_PRODUCT1_JSON =f"{PATH_OUTPUT_PRODUCT}/en_product1.json"
PATH_OUTPUT_DF_PRODUCT1 =f"{PATH_OUTPUT_PRODUCT}/en_product1.xlsx"

# Input product
PATH_INPUT_PRODUCT = os.path.join(PATH_INPUT, "pd_orphanet")
os.makedirs(PATH_INPUT_PRODUCT, exist_ok=True)

PATH_INPUT_PRODUCT4RSD_XML =f"{PATH_INPUT_PRODUCT}/all_rsdpd4_mai_2025.xml"
PATH_INPUT_PRODUCT4_XML =f"{PATH_INPUT_PRODUCT}/all_enpd_mai_2025.xml"
PATH_INPUT_PRODUCT1_XML =f"{PATH_INPUT_PRODUCT}/en_product1.xml"
PATH_INPUT_PRODUCT7_XML =f"{PATH_INPUT_PRODUCT}/en_product7.xml"

PATH_INPUT_PRODUCTCLASSIF_XML = os.path.join(PATH_INPUT_PRODUCT, "Classifications")
os.makedirs(PATH_INPUT_PRODUCTCLASSIF_XML, exist_ok=True)
PATH_INPUT_PREVALENCE =f"{PATH_INPUT_PRODUCT}/prevalences.json"


PATH_INPUT_PATIENTS_FOLDER = os.path.join(PATH_INPUT, "patient", "SolveRD_WP1_phenopackets_v2_with_ern_13301")
os.makedirs(PATH_INPUT_PATIENTS_FOLDER, exist_ok=True)
PATH_INPUT_PATIENTS_FOLDER_ONTOLOGYX = os.path.join(PATH_INPUT, "patient", "study_population")
os.makedirs(PATH_INPUT_PATIENTS_FOLDER_ONTOLOGYX, exist_ok=True)

PATH_INPUT_PATIENTS_FC =f"{PATH_INPUT}/patient/PATIENTS_SOLVED_FC_v2.xlsx"
PATH_INPUT_STEP_A2 =f"{PATH_INPUT}/stepA2.tsv"


# If you have more path variables, use os.path.join everywhere and never add slashes at the start
