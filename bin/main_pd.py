

from bin.set_log import * 
from bin.classes.dataset import * 

if __name__ == "__main__":

    # -------------------------------------------------------------------------------
    #                        1. DATA LOADING AND PREPROCESSING
    #    - Load data from input phenopacket solverd
    #    - Kepp comfirmed one 
    #    - Normalize/Standardize data
    #-------------------------------------------------------------------------------
    notused_path = ''
 
    

    ################################################################################
    #####       Load json file product7                                       #####
    ################################################################################
            
    build_rds_json = DataSet("/home/maroua/Téléchargements/en_product6.xml","")
    json_rd = build_rds_json.from_xml_to_json()
    build_rds_json.save_json("/home/maroua/Bureau/my_pipeline_v3/GSSM_DRW/output/pd_orphanet/en_product6.json", json_rd) 

    
    df_pd6 = build_gene.df_pd6()
    df_pd6.to_excel("/home/maroua/Bureau/my_pipeline_v3/GSSM_DRW/output/pd_orphanet/en_product6.xlsx")



 
 