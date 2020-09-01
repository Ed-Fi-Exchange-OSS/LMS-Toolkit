import pandas as pd
import os

def ToCsv(data, name):
    df = pd.DataFrame(data)
    file_name = f"{name}.csv"
    output_path = os.getenv("CSV_OUTPUT_PATH")

    df.to_csv(f"{output_path}/{file_name}", index=False)
    print(f"The file has been generated => {file_name}")
