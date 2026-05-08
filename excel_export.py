import pandas as pd
from datetime import datetime

def export_excel(res):
    df = pd.DataFrame([res])
    fname = f"HP_Design_{datetime.now():%Y%m%d_%H%M%S}.xlsx"
    df.to_excel(fname, index=False)