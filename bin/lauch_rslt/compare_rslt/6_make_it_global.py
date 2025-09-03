

from bin.set_log import * 
from bin.path_variable import (
    PATH_OUTPUT_COMPARE_METRIC_CLASSIF,
    PATH_OUTPUT_COMPARE_GLOBAL,
)

print(f"\n\n############################################")
print(f"\n\n############################################")
print(f"START  6_make_it_global")
print(f"START  6_make_it_global")

t0 = time.perf_counter()

os.makedirs(PATH_OUTPUT_COMPARE_GLOBAL , exist_ok=True)

path_xlsx = PATH_OUTPUT_COMPARE_METRIC_CLASSIF + "/xlsx/"
 
list_patient = os.listdir(path_xlsx)
list_patient_f = []
for onep in list_patient:
    if '~' not in onep:
        list_patient_f.append(onep)


list_df4 = []
for one_p in list_patient_f:
 
    df_classif_grp_rd = pd.read_excel(path_xlsx + one_p ,sheet_name='classif',index_col=0)


 
    list_df4.append(df_classif_grp_rd)

 
df_global_classif = pd.concat(list_df4)

len(df_global_classif['type'].drop_duplicates())

## save en mode global sans filtration
df_global_classif.to_excel(PATH_OUTPUT_COMPARE_GLOBAL + "/global_classif.xlsx")
 

print(f"END  6_make_it_global done in {time.perf_counter() - t0:.1f}s")
print(f"END  6_make_it_global done in {time.perf_counter() - t0:.1f}s")
