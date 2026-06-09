import pandas as pd
import os

folder = "dataset/raw_extracted"

all_questions = []

for file in os.listdir(folder):

    if file.endswith(".csv"):

        # Skip syllabus for now
        if file == "OS_syllabus.csv":
            continue

        path = os.path.join(folder, file)

        df = pd.read_csv(path)

        all_questions.append(df)

master = pd.concat(all_questions, ignore_index=True)

master = master.drop_duplicates()

master.to_csv(
    "dataset/master_questions.csv",
    index=False
)

print("Total unique questions:", len(master))