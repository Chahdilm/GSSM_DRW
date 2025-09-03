
from bin.set_log import * 
from bin.path_variable import PATH_OUTPUT_HM

logger.info(f"\n\n############################################")
print(f"\n\n############################################")

print(f"START  14_harmonic_mean_concat")
logger.info(f"START  14_harmonic_mean_concat")

t0 = time.perf_counter()

#########################################################################
# # Set up argument parsing
parser = argparse.ArgumentParser(description="Process inputs for the script.")

# # Arguments 
parser.add_argument("--topn",type=int,required=True,)
parser.add_argument("--hierarchy_level",type=int,required=True,)

# # Parse the arguments
args = parser.parse_args()

topn = args.topn  
hierarchy_level = args.hierarchy_level  
########################################################################
# topn = 10
# hierarchy_level =  1

########################################################################
list_output = os.listdir(PATH_OUTPUT_HM)
list_rslt = []
for el in list_output:
    if (".xlsx" in el )and ('hm_' in el) and (f'_{hierarchy_level}_' in el):
        list_rslt.append(el)


big_df = []
for onedf in list_rslt:
    print(onedf)
    df = pd.read_excel(PATH_OUTPUT_HM + "/" + onedf,index_col=0)   
    big_df.append(df)
df_rslt = pd.concat(big_df)
df_rslt = df_rslt.sort_values(by=['method']).drop_duplicates(subset=['method'])

df_rslt.to_excel(f"{PATH_OUTPUT}/concat_hm_level_{hierarchy_level}_top_{topn}.xlsx")