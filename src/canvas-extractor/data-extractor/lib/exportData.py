# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import pandas as pd
import os

def ToCsv(data, name):
    df = pd.DataFrame(data)
    file_name = f"{name}.csv"
    output_path = os.getenv("DATA_EXTRACTOR_CSV_OUTPUT_PATH")

    df.to_csv(f"{output_path}/{file_name}", index=False)
    print(f"The file has been generated => {file_name}")
