import pandas as pd

# Load questions
questions_df = pd.read_csv("dataset/master_questions.csv")

# Topic → CO mapping
topic_df = pd.read_csv("dataset/co_topics.csv")

co_data = []

for question in questions_df["question"]:

    q = str(question).lower()

    assigned_co = None

    for _, row in topic_df.iterrows():

        topic = str(row["topic"]).lower()
        co = row["co"]

        topic_words = topic.split()

        for word in topic_words:

            if len(word) > 3 and word in q:
                assigned_co = co
                break

        if assigned_co:
            break

    if assigned_co:
        co_data.append({
            "question": question,
            "co": assigned_co
        })

co_df = pd.DataFrame(co_data)

co_df.to_csv(
    "dataset/co_dataset.csv",
    index=False
)

print("\nCO Dataset Created")
print(co_df["co"].value_counts())
print("\nTotal Questions:", len(co_df))