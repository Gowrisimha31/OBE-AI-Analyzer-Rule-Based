import pandas as pd

df = pd.read_csv("dataset/co_dataset.csv")

print(df.sample(30))