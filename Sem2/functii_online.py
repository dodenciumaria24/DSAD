import numpy as np
import pandas as pd

def nan_replace_df(tabel: pd.DataFrame)->pd.DataFrame:
    # fac o copie tabelului
    df_curat=tabel.copy()
#     selectez col numerice
    col_numerice=df_curat.select_dtypes(include=[np.number])
#     pt fiecare val NaN, o inlocuiesc cu media coloanei
    for col in col_numerice.columns:
        media=col_numerice[col].mean()
        df_curat[col]=df_curat[col].fillna(media)
    return df_curat
