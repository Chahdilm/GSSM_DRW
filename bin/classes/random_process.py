from set_log import *




class RandomWalker:
    """Performs one alpha-PageRank on one patient’s matrix."""
    def __init__(self, matrix_dir, output_dir, alpha, classification_json):
        self.matrix_dir         = matrix_dir
        self.output_dir         = output_dir
        self.alpha              = alpha
        self.class_count        = self.load_classification(classification_json)
        os.makedirs(self.output_dir, exist_ok=True)

    def load_classification(self, path):
    
        # Load classification data and build count per RD
        data_classif = json.load(open(path))
        class_count = {}
        for cls, rds in data_classif.items():
            for rd in rds:
                class_count[rd] = class_count.get(rd, 0) + 1
        return class_count

    def build_graph(self, seed_id):
         # Load adjacency matrix for the first seeds to build the graph once
        csv_path = os.path.join(self.matrix_dir, f"{seed_id}.csv")
        df_m     = pd.read_csv(csv_path, index_col=0)
        # Build NetworkX graph
        G_raw    = nx.from_pandas_adjacency(df_m)
        G_raw.remove_edges_from(nx.selfloop_edges(G_raw))

        # normalize rows
        A       = nx.adjacency_matrix(G_raw).toarray()
        df_adj  = pd.DataFrame(A, index=df_m.index, columns=df_m.index)
        df_adj['tot'] = df_adj.sum(axis=1)
        df_norm = (df_adj.div(df_adj['tot'], axis=0).drop(columns=['tot'])    )
        return nx.from_pandas_adjacency(df_norm), df_norm.sum().sort_values(ascending=False)

    def run_for_seed(self, seed_id):
        """Run PageRank for one seed and write <seed>.xlsx."""
        # Precompute sum of normalized degrees with sum_degres
        G, sum_degres = self.build_graph(seed_id)
        personalization = {n: (1 if n == seed_id else 0) for n in G.nodes()}

         # Run PageRank once per alpha
        t0 = time.perf_counter()
        pr = nx.pagerank(G, alpha=self.alpha, personalization=personalization)
        pr.pop(seed_id, None)

         # Build result DataFrame
        df_pr = (
            pd.Series(pr, name='pg').to_frame()
            .assign(
                sum_degres=lambda df: df.index.map(sum_degres),
                nb_classif=lambda df: df.index.map(lambda rd: self.class_count.get(rd, 0))
            )
        )
        df_pr['rank_pg'] = df_pr['pg'].rank(ascending=False, method='min')
        df_pr['rank_sum_degres_pg'] = df_pr['sum_degres'].rank(ascending=False, method='min')

        out_path = os.path.join(self.output_dir, f"{seed_id}.xlsx")
        df_pr.to_excel(out_path, engine='openpyxl')
        print("Seed %s done in %.1fs → %s", seed_id, time.perf_counter()-t0, out_path)


class RandomWalkBatch:
    """Runs a batch of RandomWalker jobs for multiple seeds."""
    def __init__(self, seeds, alpha, matrix_subdir,path_integrate_p,path_folder_rw,path_classif):
        self.seeds            = seeds
        self.alpha            = alpha
        self.matrix_subdir    = matrix_subdir
        self.matrix_dir       = os.path.join(path_integrate_p, matrix_subdir)
        self.output_dir       = os.path.join(path_folder_rw, str(alpha), matrix_subdir)
        self.path_classif            = path_classif

    def run(self):
        walker = RandomWalker(
            matrix_dir=self.matrix_dir,
            output_dir=self.output_dir,
            alpha=self.alpha,
            classification_json=self.path_classif,
        )


        extract_seed = {f.split('.')[0] for f in os.listdir(self.output_dir)}
        first_seed = self.seeds[0]
        if first_seed in extract_seed:
            logging.warning("First seed %s already done → skipping batch", first_seed)
            return

        for seed in self.seeds:
            walker.run_for_seed(seed)


class RandomWalkAggregator:
    """Aggregates all per-patient RW outputs into a single summary."""
    def __init__(self, matrix_subdir, alpha,df_patient,path_folder_rw):
        self.alpha         = str(alpha)
        self.matrix_subdir = matrix_subdir
        self.rw_dir        = os.path.join(path_folder_rw, self.alpha, matrix_subdir)
        self.df_patient    =df_patient
        self.path_folder_rw = path_folder_rw

    def aggregate(self):
        files = [f for f in os.listdir(self.rw_dir) if f.endswith(".xlsx")]
        pairs = []
        for fname in files:
            patient_id = fname[:-5]
            subset    = self.df_patient[self.df_patient['phenopacket'] == patient_id]
            try:
                rdi = subset['Disease'].iloc[0]
                df  = pd.read_excel(os.path.join(self.rw_dir, fname))
                score = df.loc[df['RD'] == rdi, 'pg'].iat[0]
                rank  = int(df.loc[df['RD'] == rdi, 'rank_pg'].iat[0])
                pairs.append((patient_id, rdi, score, rank))
            except Exception:
                logging.warning("Skipping %s: no matching RD in output", fname)

        df_out = pd.DataFrame(pairs, columns=['patients','RDs','score','rank'])
        out_path = os.path.join(self.path_folder_rw, self.alpha, f"RARW_{self.matrix_subdir}.xlsx")
        df_out.to_excel(out_path, engine='openpyxl')
        print("Aggregated %d patients → %s", len(df_out), out_path)




