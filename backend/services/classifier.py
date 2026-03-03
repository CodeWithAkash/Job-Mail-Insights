import os
import joblib
import re
import string


MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "ml",
    "email_classifier.pkl"
)


def clean_text(text):
    text = text.lower()
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'\r', ' ', text)
    text = re.sub(r'\d+', '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = re.sub(r'\s+', ' ', text).strip()
    return text


class EmailClassifier:
    _model = None

    def __init__(self):
        if EmailClassifier._model is None:
            EmailClassifier._model = joblib.load(MODEL_PATH)

        self.model = EmailClassifier._model

    def classify(self, subject, body):
        try:
            text = clean_text(f"{subject} {body}")
            prediction = self.model.predict([text])[0]
            return prediction

        except Exception as e:
            print("Classification error:", e)
            return "Pending"