import os
import joblib


MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "ml",
    "email_classifier.pkl"
)


class EmailClassifier:
    _model = None

    def __init__(self):
        if EmailClassifier._model is None:
            EmailClassifier._model = joblib.load(MODEL_PATH)

        self.model = EmailClassifier._model

    def classify(self, subject, body):
        try:
            text = f"{subject} {body}"
            prediction = self.model.predict([text])[0]
            return prediction
        except Exception as e:
            print("Classification error:", e)
            return "Pending"