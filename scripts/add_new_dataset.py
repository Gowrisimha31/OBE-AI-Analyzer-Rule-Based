import pandas as pd

# Load new dataset
new_df = pd.read_csv("os_dataset.csv")

# -----------------------------
# BLOOM DATASET
# -----------------------------

bloom_map = {
    "L1": "Remember",
    "L2": "Understand",
    "L3": "Apply",
    "L4": "Analyze",
    "L5": "Evaluate",
    "L6": "Create"
}

new_bloom = pd.DataFrame({
    "question": new_df["question"],
    "bloom_level": new_df["BTL"].map(bloom_map)
})

old_bloom = pd.read_csv(
    "dataset/bloom_dataset.csv"
)

combined_bloom = pd.concat(
    [old_bloom, new_bloom],
    ignore_index=True
)

combined_bloom.drop_duplicates(
    subset=["question"],
    inplace=True
)

combined_bloom.to_csv(
    "dataset/bloom_dataset.csv",
    index=False
)

print(
    "Bloom Dataset Size:",
    len(combined_bloom)
)

# -----------------------------
# CO DATASET
# -----------------------------

new_co = pd.DataFrame({
    "question": new_df["question"],
    "co": new_df["CO"]
})

old_co = pd.read_csv(
    "dataset/co_dataset.csv"
)

combined_co = pd.concat(
    [old_co, new_co],
    ignore_index=True
)

combined_co.drop_duplicates(
    subset=["question"],
    inplace=True
)

combined_co.to_csv(
    "dataset/co_dataset.csv",
    index=False
)

print(
    "CO Dataset Size:",
    len(combined_co)
)

print("\nDataset Merge Complete")