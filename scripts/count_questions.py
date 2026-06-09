import pandas as pd
import os

folder = "dataset/raw_extracted"

total = 0

for file in os.listdir(folder):
    if file.endswith(".csv"):
        df = pd.read_csv(os.path.join(folder, file))
        print(f"{file}: {len(df)} questions")
        total += len(df)

print("\nTotal Questions:", total)