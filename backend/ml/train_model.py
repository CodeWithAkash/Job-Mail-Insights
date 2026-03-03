import pandas as pd
import joblib
import re
import string

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report


# ---------- TEXT CLEANING FUNCTION ----------
def clean_text(text):
    text = text.lower()
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'\r', ' ', text)
    text = re.sub(r'\d+', '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = re.sub(r'\s+', ' ', text).strip()
    return text


# ---------- LOAD DATA ----------
df = pd.read_csv("ml/training_data.csv")

df["text"] = df["text"].apply(clean_text)

X = df["text"]
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# ---------- STRONG MODEL PIPELINE ----------
model = Pipeline([
    ("tfidf", TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 3),        # Unigram + Bigram + Trigram
        max_features=10000,       # Increased feature space
        min_df=2,                 # Ignore rare noise
        max_df=0.9                # Ignore too frequent words
    )),
    ("clf", LinearSVC(
        C=1.5,                    # Stronger margin
        class_weight="balanced"
    ))
])


# ---------- TRAIN ----------
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print("\n===== MODEL PERFORMANCE =====")
print(classification_report(y_test, y_pred))

joblib.dump(model, "ml/email_classifier.pkl")

print("✅ Strong NLP Model Trained and Saved")