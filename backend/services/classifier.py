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
            print("Loading ML model from:", MODEL_PATH)
            EmailClassifier._model = joblib.load(MODEL_PATH)

        self.model = EmailClassifier._model

    def classify(self, subject, body):
        text = f"{subject} {body}".strip()

        if len(text) < 10:
            return "Pending"

        prediction = self.model.predict([text])[0]

        print("CLASSIFICATION DEBUG:")
        print("TEXT:", text[:150])
        print("PREDICTION:", prediction)

        return prediction