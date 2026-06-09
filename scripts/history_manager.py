import csv
import os
from datetime import datetime

HISTORY_FILE = "dataset/prediction_history.csv"


def save_prediction(question, bloom, co, po):

    file_exists = os.path.exists(HISTORY_FILE)

    with open(
        HISTORY_FILE,
        "a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        if not file_exists:

            writer.writerow([
                "timestamp",
                "question",
                "bloom",
                "co",
                "po"
            ])

        writer.writerow([
            datetime.now(),
            question,
            bloom,
            co,
            ", ".join(po)
        ])