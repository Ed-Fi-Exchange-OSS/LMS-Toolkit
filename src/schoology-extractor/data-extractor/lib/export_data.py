import pandas as pd


def tocsv(data, output_path):
    df = pd.DataFrame(data)

    df.to_csv(output_path, index=False)
    # TODO: implement logging
    print(f"The file has been generated => {output_path}")
