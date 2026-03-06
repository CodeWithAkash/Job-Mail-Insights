import os
import pandas as pd
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report


BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, "training_data.csv")
MODEL_PATH = os.path.join(BASE_DIR, "email_classifier.pkl")

print("Loading dataset from:", DATA_PATH)

df = pd.read_csv(DATA_PATH)

print("Dataset size:", len(df))

X = df["text"]
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("Training model...")

pipeline = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 3),
            max_features=8000,
            min_df=2
        )
    ),
    (
        "clf",
        LogisticRegression(
            max_iter=2000,
            class_weight="balanced"
        )
    )
])

pipeline.fit(X_train, y_train)

print("\nEvaluating model...\n")

y_pred = pipeline.predict(X_test)

print(classification_report(y_test, y_pred))

joblib.dump(pipeline, MODEL_PATH)

print("\nModel saved to:", MODEL_PATH)
print("Training completed successfully.")