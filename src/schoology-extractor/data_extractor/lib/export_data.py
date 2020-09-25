import pandas as pd


def tocsv(data, output_path):
    """
    Args:
        data (dictionary): The data that will be expoted to csv
        output_path (dictionary): The path and name where you want your csv to be generated
    """
    assert data is not None
    assert output_path is not None

    df = pd.DataFrame(data)

    df.to_csv(output_path, index=False)
    print(f"The file has been generated => {output_path}")
