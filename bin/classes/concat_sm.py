from set_log import * 
from pathlib import Path


class ConcatSm():
    def __init__(self,vector_str,col1,col2):
        self.vector_str = vector_str
        self.col1 = col1
        self.col2 = col2
 



    def process_similarity(self, base_dir,pdtype_pattern):
        """Concat & rank SM/CDF outputs under base_dir for the given vector_str."""
        xlsx_files = glob.glob(f"{base_dir}/**/*.xlsx", recursive=True)
        data_dict = {}

        combine_opts = {'BUMS','rsd','funSimAvg','BMA','funSimMax'}
        sm_methods   = {'resnik','graphic','rel','ic','lin','jc'}
        weights      = {'n'}

        for f in xlsx_files:
            combine = sm_method = weight = pdtype = None
            for part in Path(f).parts:
                if part in combine_opts:
                    combine = part
                elif part in sm_methods:
                    sm_method = part
                elif part in weights:
                    weight = part
                elif pdtype_pattern in part:
                    pdtype = part

            if None in (combine, sm_method, weight, pdtype):
                logging.warning("Skipping %s: missing component", f)
                continue

            key = f"{self.vector_str}_{combine}_{sm_method}_{weight}_{pdtype}"
            data_dict.setdefault(key, []).append(f)

        for key, files in data_dict.items():
            start = time.perf_counter()
            dfs_sm, dfs_cdf = [], []

            for fn in files:
                try:
                    df = pd.read_excel(fn, index_col=0)
                    if df.empty:
                        continue
                    (dfs_cdf if "CDF" in fn else dfs_sm).append(df)
                except Exception as e:
                    logging.warning("Error reading %s: %s", fn, e)

            if not dfs_sm:
                logging.warning("[%s] no SM files to concatenate", key)
                continue

            # concat & rank
            df_sm = pd.concat(dfs_sm)
            df_sm = (
                df_sm
                .sort_values([self.col1, "score"], ascending=[True, False])
                .assign(rank=lambda d: d.groupby(self.col1)["score"]
                                .rank(ascending=False, method="dense"))
            )
            out_sm = os.path.join(base_dir, f"{key}.xlsx")
            df_sm.to_excel(out_sm)
            logging.info("Wrote %s (%.1fs)", out_sm, time.perf_counter() - start)

            # merge & write CDF if present
            if dfs_cdf:
                try:
                    df_cdf = (
                        pd.concat(dfs_cdf)
                        .merge(df_sm, on=[self.col1, self.col2], how="left")
                        .dropna()
                    )
                    out_cdf = os.path.join(base_dir, f"CDF_{key}.xlsx")
                    df_cdf.to_excel(out_cdf)
                    logging.info("Wrote %s", out_cdf)
                except Exception as e:
                    logging.warning("[%s] failed to produce CDF: %s", key, e)



    def concat_matrix(self,base_dir):
        """Pivot & concatenate MM score matrices under base_dir for the given vector_str."""
        xlsx_files = glob.glob(f"{base_dir}/**/*.xlsx", recursive=True)
 
        rows = []
        for f in xlsx_files:
            if self.vector_str not in f:
                continue
            try:
                df = pd.read_excel(f, usecols=[self.col1, self.col2, "score"])
                rows.append(df.pivot(index=self.col1, columns=self.col2, values="score"))
            except Exception as e:
                logging.warning("Skipping %s: %s", f, e)

        if not rows:
            logging.error("No valid matrices found for %s", self.vector_str)
            return

        mat = pd.concat(rows).dropna()
        labels = sorted(set(mat.index) | set(mat.columns))
        mat = mat.reindex(index=labels, columns=labels, fill_value=0)
        out_path = Path(base_dir) / f"{self.vector_str}_concat_matrix.xlsx"
        mat.to_excel(out_path)
        print("Wrote concatenated matrix to %s", out_path)

