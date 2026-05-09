import pandas as pd

def export_excel(data, filename="process_card.xlsx"):
    """
    Exports design results to an Excel file.
    """
    df = pd.DataFrame([data])
    # In a real application, you would format this into a proper template
    df.to_excel(filename, index=False)
    print(f"Exported {filename}")
    return filename
