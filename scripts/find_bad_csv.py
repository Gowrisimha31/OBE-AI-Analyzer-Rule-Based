import pandas as pd
import os

folder = "dataset/raw_extracted"

for file in os.listdir(folder):
    if file.endswith(".csv"):
        path = os.path.join(folder, file)

        try:
            df = pd.read_csv(path)
            print(f"✓ {file}")
        except Exception as e:
            print(f"✗ {file}")
            print(e)
            print("-" * 50)