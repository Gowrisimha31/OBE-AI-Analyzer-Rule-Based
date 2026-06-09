import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, accuracy_score

# Load dataset
df = pd.read_csv("dataset/bloom_dataset.csv")

X = df["question"]
y = df["bloom_level"]

# Better TF-IDF
vectorizer = TfidfVectorizer(
    ngram_range=(1, 2),
    max_features=5000,
    lowercase=True
)

X_vec = vectorizer.fit_transform(X)

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X_vec,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Train model
model = MultinomialNB()

model.fit(X_train, y_train)

# Predict
predictions = model.predict(X_test)

print("\nAccuracy:")
print(accuracy_score(y_test, predictions))

print("\nClassification Report:")
print(classification_report(y_test, predictions))

# Save model
joblib.dump(
    model,
    "models/bloom_model.pkl"
)

joblib.dump(
    vectorizer,
    "models/bloom_vectorizer.pkl"
)

print("\nBloom Model Saved Successfully")