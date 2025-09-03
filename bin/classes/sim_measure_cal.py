from bin.set_log import * 

 

class Sim_measure():
    def __init__(self,df_group1,df_group2,colname_1,colname_2):
        #self.dict_ic = dict_ic
        self.df_group1 = df_group1
        self.df_group2 = df_group2
        self.colname_1  = colname_1
        self.colname_2  = colname_2

    ############################################################
    #####                  calcul section                  #####
    ############################################################


    #############################################################################
    ####              calcul section                        PHASE TWO        ####
    #############################################################################


    def iterative_bums(self,score_array):
        result_bums = {}
        # print(f"Starting : \n{score_array}\n")
        ## Number of elements in the array are not egal to 0 
        while score_array.size > 0:
            max_in_array =  np.amax(score_array) # max for col
            # print(f"max_in_array :\n {max_in_array}")
            max_index = np.where(score_array ==max_in_array)
            # print(f"Max index :\n {max_index}")

            ## Store the result (index and value)
            result_bums[str(max_index[0][0]) + " - " +  str(max_index[1][0])] = max_in_array
            # print(f'Rslt BUMS in t instant \n{result_bums}')
            ## Remove section 
            score_array = np.delete(score_array, max_index[0], axis=0)  # Remove row
            # print(f"Row removed \n{score_array}")
            score_array = np.delete(score_array, max_index[1], axis=1)  # Remove column
            # print(f"col removed \n{score_array}")

        #print("BUMS process:\n", result_bums)
        return result_bums

    def set_freq_for_sm(self,one_hpo_valid,the_mini_df,vector_weight,is_freq):
        try:
            #temp_df = minidf_2.set_index('hpo_id').drop_duplicates()
            temp_df = the_mini_df[the_mini_df['hpo_id'] == one_hpo_valid.id]['hpo_frequency']
            hpo_frequency = temp_df.values[0]
            #logger.info(f"({one_hpo_valid.id}\t Freq : {hpo_frequency}")
            add_weight=1
            if (hpo_frequency == 1) : 
                # Obligate  5/5
                add_weight = vector_weight[0] 
            elif  (hpo_frequency == 0.8) : 
                # Very frequent 4/5 
                add_weight = vector_weight[1] 
            elif  hpo_frequency == 0.6  :
                # Frequent3/5
                add_weight = vector_weight[2]  
            elif hpo_frequency == 0.4:
                # Occasional 2/5
                add_weight = vector_weight[3]  
                # Very rare  1/5
            elif hpo_frequency ==0.2:
                add_weight = vector_weight[4]    

        except KeyError:
            hpo_frequency_el = 1
        
        if is_freq == "y":
            hpo_frequency_el = hpo_frequency * add_weight
        if is_freq == "n":
            hpo_frequency_el =  add_weight
        
        #logger.info(f"AFTER \t{one_hpo_valid.id}\t Freq : {hpo_frequency_el}")

        return hpo_frequency_el



    def run_sm_freq(self,element2,patient_id_list,combine,method,is_freq,vector_weight): # rajouter un vecteur ici pour les frequences 
        combine_method_rsl = 0

        hpo_frequency_el1 = hpo_frequency_el2 = 1
        # add poid frequence vecteur c'est pas le hpo frequency

        interaction_all = set()
        ## usually a loop here but the loop will be done on the snakefile

        minidf_2 = self.df_group2[self.df_group2[self.colname_2]==element2]
        hpo_el_2 = minidf_2['hpo_id'].drop_duplicates().tolist() 
        hpo_excluded = minidf_2[minidf_2['hpo_frequency'] == 0]['hpo_id'].drop_duplicates().tolist()

        for e1,element1 in enumerate(patient_id_list):
            if element2 == element1 : 
                combine_method_rsl = 0
            else:
                minidf_1 = self.df_group1[self.df_group1[self.colname_1]==element1]
                hpo_el_1 = minidf_1['hpo_id'].drop_duplicates().tolist() 

                ## test if the patients as hpo excluded if true no need to make sm the result will be 0
                is_match_excluded = set(hpo_excluded).intersection(hpo_el_1)
                if len(is_match_excluded) != 0:
                    ## the patient have at least one  hpo excluded from disease -> he don t have the disease
                    combine_method_rsl = 0
                    #print(f"{element2} - {element1} : excluded  ")

                else:
                    ## implement matrix 
                    score_matrix = np.zeros(shape=(len(hpo_el_2), len(hpo_el_1))) # row,col

                    for i,one_hpo_2 in enumerate(hpo_el_2):
                        try:  # try/except hpo term invalid
                            one_hpo_rd_term = Ontology.get_hpo_object(one_hpo_2)
                            hpo_frequency_el2 = self.set_freq_for_sm(one_hpo_rd_term,minidf_2,vector_weight,is_freq)

                            for j,one_hpo_1 in enumerate(hpo_el_1):
                                try :  # try/except hpo term invalid
                                    one_hpo_p_term = Ontology.get_hpo_object(one_hpo_1)
                                    finale_score = 0

                                    ## build matrix 
                                    ic_mica = one_hpo_rd_term.similarity_score(one_hpo_p_term, 'orpha', method)
                                    finale_score = ic_mica * hpo_frequency_el1 * hpo_frequency_el2 # patient have a frequency of 1 

                                    score_matrix[i, j] = finale_score

                                    #print(f"Score between RD : {element1} - Patient :{element2} :{one_hpo_rd_term.id}  and {one_hpo_p_term.id}: {score_matrix[i, j]} \n")   


                                except RuntimeError:
                                    #logger.info(f"Hpo term invalid : {one_hpo_2}")
                                    ic_mica = 0                       
                        except RuntimeError:
                            #logger.info(f"Hpo term invalid : {one_hpo_1}")
                            ic_mica = 0

                        # max for each row 
                        max_row = np.amax(score_matrix, axis=1)
                        # max for each col 
                        max_col = np.amax(score_matrix, axis=0)
                        if combine == "funSimAvg":
                            combine_method_rsl = ((sum(max_row) / len(max_row)) + (sum(max_col) / len(max_col))) / 2

                        if combine == "funSimMax":
                            combine_method_rsl =  max([sum(max_row) / len(max_row), sum(max_col) / len(max_col)])

                        if combine == "BMA": 
                            combine_method_rsl= (sum(max_row) + sum(max_col)) / (len(max_row) + len(max_col))
                        if combine == "BUMS":      
                            bums = self.iterative_bums(score_matrix)
                            combine_method_rsl = sum(bums.values())/ len(hpo_el_1)
                        if combine == "rsd":
                            # For patient → disease: for each patient‐HPO term (each column) take the best disease match
                            combine_method_rsl = sum(max_col) / len(hpo_el_1)
                        
                        #logger.info(f"{element2} - {element1} \t {combine}\t{combine_method_rsl}")
                        #logger.info(f"{element2} - {element1} \t {combine}\t Score {combine_method_rsl} \t max col : {max_col}\tm max row : {max_row}")

                        #logger.info(f"{element2} - {element1} \t {combine}\t{combine_method_rsl} \n{score_matrix}")

                
            ## build the result matrix here  put condition if here 
            #matrix_sm[e1, e2] = combine_method_rsl  #round(combine_method_rsl,2)
            interaction_all.add((element2,element1,combine_method_rsl))
        df_mp = pd.DataFrame(interaction_all,columns=['RDs','patients','score'])



        return df_mp




    def run_mm_freq(self,element2,patient_id_list,combine,method,is_freq,vector_weight): # rajouter un vecteur ici pour les frequences 
        combine_method_rsl = 0

        hpo_frequency_el1 = hpo_frequency_el2 = 1
        # add poid frequence vecteur c'est pas le hpo frequency

        interaction_all = set()
        ## usually a loop here but the loop will be done on the snakefile

        minidf_2 = self.df_group2[self.df_group2[self.colname_2]==element2]
        hpo_el_2 = minidf_2['hpo_id'].drop_duplicates().tolist() 
        hpo_excluded = minidf_2[minidf_2['hpo_frequency'] == 0]['hpo_id'].drop_duplicates().tolist()

        for e1,element1 in enumerate(patient_id_list):
            if element2 == element1 : 
                combine_method_rsl = 0
            else:
                minidf_1 = self.df_group1[self.df_group1[self.colname_1]==element1]
                hpo_el_1 = minidf_1['hpo_id'].drop_duplicates().tolist() 

                ## implement matrix 
                score_matrix = np.zeros(shape=(len(hpo_el_2), len(hpo_el_1))) # row,col

                for i,one_hpo_2 in enumerate(hpo_el_2):
                    try:  # try/except hpo term invalid
                        one_hpo_rd_term = Ontology.get_hpo_object(one_hpo_2)
                        hpo_frequency_el2 = self.set_freq_for_sm(one_hpo_rd_term,minidf_2,vector_weight,is_freq)

                        for j,one_hpo_1 in enumerate(hpo_el_1):
                            try :  # try/except hpo term invalid
                                one_hpo_p_term = Ontology.get_hpo_object(one_hpo_1)
                                finale_score = 0

                                ## build matrix 
                                ic_mica = one_hpo_rd_term.similarity_score(one_hpo_p_term, 'orpha', method)
                                finale_score = ic_mica * hpo_frequency_el1 * hpo_frequency_el2 # patient have a frequency of 1 

                                score_matrix[i, j] = finale_score

                                #print(f"Score between RD : {element1} - Patient :{element2} :{one_hpo_rd_term.id}  and {one_hpo_p_term.id}: {score_matrix[i, j]} \n")   


                            except RuntimeError:
                                #logger.info(f"Hpo term invalid : {one_hpo_2}")
                                ic_mica = 0                       
                    except RuntimeError:
                        #logger.info(f"Hpo term invalid : {one_hpo_1}")
                        ic_mica = 0

                    # max for each row 
                    max_row = np.amax(score_matrix, axis=1)
                    # max for each col 
                    max_col = np.amax(score_matrix, axis=0)
                    if combine == "funSimAvg":
                        combine_method_rsl = ((sum(max_row) / len(max_row)) + (sum(max_col) / len(max_col))) / 2

                    if combine == "funSimMax":
                        combine_method_rsl =  max([sum(max_row) / len(max_row), sum(max_col) / len(max_col)])

                    if combine == "BMA": 
                        combine_method_rsl= (sum(max_row) + sum(max_col)) / (len(max_row) + len(max_col))
                    if combine == "BUMS":      
                        bums = self.iterative_bums(score_matrix)
                        combine_method_rsl = sum(bums.values())/ len(hpo_el_1)
                    if combine == "rsd":
                        # For patient → disease: for each patient‐HPO term (each column) take the best disease match
                        combine_method_rsl = sum(max_col) / len(hpo_el_1)

                
            ## build the result matrix here  put condition if here 
            #matrix_sm[e1, e2] = combine_method_rsl  #round(combine_method_rsl,2)
            interaction_all.add((element2,element1,combine_method_rsl))
        df_mp = pd.DataFrame(interaction_all,columns=['RDs','patients','score'])



        return df_mp




    def export_sm(self,df,path_output):
        df.to_excel(path_output )


    def from_sm_make_cdf(self,df_sm,col_name):
        ## Filter the df patients
        df_patient_confirmed = self.df_group1[[self.colname_1,col_name]]  # Disease pour col_name
        df_patient_confirmed.columns = ["patients","RDs"] 
        df_patient_confirmed = df_patient_confirmed.drop_duplicates()
        
        df_cdf = pd.merge(df_sm[["patients","RDs"]], df_patient_confirmed, how='inner', on=["RDs","patients"]).dropna()
        # print("Nb Patients {}\t Nb diseases : {} ".format(len(df_cdf['patients'].drop_duplicates().tolist()), len(df_cdf['RDs'].drop_duplicates().tolist())))
        return df_cdf

    def from_mm_make_cdf(self,df_sm):
        ## Filter the df patients
        df_rd = self.df_group1[[self.colname_1,'ORPHAcode']] 
        df_rd.columns = ["patients","RDs"] 
        df_rd = df_rd.drop_duplicates()
        
        df_cdf = pd.merge(df_sm[["patients","RDs"]], df_rd, how='inner', on=["RDs","patients"]).dropna()
        # print("Nb Patients {}\t Nb diseases : {} ".format(len(df_cdf['patients'].drop_duplicates().tolist()), len(df_cdf['RDs'].drop_duplicates().tolist())))
        return df_cdf

 

    #############################################################################
    ####               make ra                  (call previous methods )     ####
    #############################################################################
    # this methods are use in snakefile 
 
    def compute_sm_cdf(self,index,rd,patients,patients_rds,combine,method,is_freq,weights,out_dir):
        """Compute SM table and CDF (if applicable), export both as Excel."""
        rd_file = rd.replace(":", "-")
        df_sm = self.run_sm_freq(rd, patients, combine, method, is_freq, weights)

        sm_path =  f"{out_dir}/{index}_{rd_file}.xlsx"
        self.export_sm(df_sm, sm_path)
        print("Exported SM to %s", sm_path)

        # CDF only if this RD occurs in patient list
        if rd in patients_rds:
            df_cdf = self.from_sm_make_cdf(df_sm,"Disease")
        else:
            df_cdf = pd.DataFrame(columns=["patients","RDs"], index=[0])

        cdf_path =  f"{out_dir}/CDF_{index}_{rd_file}.xlsx"
        self.export_sm(df_cdf, cdf_path)
        print("Exported CDF to %s", cdf_path)



    def compute_sm(self, index, rd, rd_id_list_2, combine, method, is_freq, weights, out_dir):
        """
        Compute similarity-measure table for mm export as excel file.
        """
        rd_file = rd.replace(":", "-")

        # 1. Compute & export SM
        df_sm = self.run_mm_freq(rd, rd_id_list_2, combine, method, is_freq, weights)
        df_sm.rename({'patients':'OC2','RDs':'OC1'}, axis='columns',inplace=True)

        sm_path = f"{out_dir}/{index}_{rd_file}.xlsx"
        self.export_sm(df_sm, sm_path)
        print(f"Exported SM to {sm_path}")
