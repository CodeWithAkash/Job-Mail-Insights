import os
import joblib

BASE_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE_DIR, "..", "ml", "email_classifier.pkl")

class EmailClassifier:

    _model = None

    def __init__(self):
        if EmailClassifier._model is None:
            print("Loading ML model...")
            EmailClassifier._model = joblib.load(MODEL_PATH)

        self.model = EmailClassifier._model

    def classify(self, subject, body):

        text = f"{subject} {body}".strip()

        if not text:
            return "Pending"

        try:
            prediction = self.model.predict([text])[0]
            return prediction
        except Exception as e:
            print("Classification error:", e)
            return "Pending"