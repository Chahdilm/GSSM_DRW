import os 
current_dir = os.getcwd()
print(current_dir)
path_act = "/home/maroua/Bureau/my_pipeline_v3/GSSM_DRW"

if not os.path.exists(path_act):
    print("Path does not exist:", path_act)
else:
    os.chdir(path_act)
    print("Current directory is now:", os.getcwd())
 