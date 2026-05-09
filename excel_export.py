import pandas as pd

def export_excel(data, filename="heat_pipe_process_card.xlsx"):
    df = pd.DataFrame([data])
    df.to_excel(filename, index=False)
    return filename
