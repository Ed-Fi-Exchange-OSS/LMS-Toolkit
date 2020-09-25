# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

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
