import os
import joblib
import re

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
            print("Loading classifier model...")
            EmailClassifier._model = joblib.load(MODEL_PATH)

        self.model = EmailClassifier._model

        # Strong keyword rules
        self.selection_patterns = [
            r"congratulations",
            r"pleased to offer",
            r"pleased to inform",
            r"thrilled to inform",
            r"you have been selected",
            r"offer letter",
            r"welcome to",
            r"job offer",
            r"selected for the position",
            r"move forward with you",
            r"interview scheduled"
        ]

        self.rejection_patterns = [
            r"regret to inform",
            r"unfortunately",
            r"not moving forward",
            r"not selected",
            r"other candidates",
            r"position has been filled",
            r"unable to proceed",
            r"application unsuccessful"
        ]

        self.pending_patterns = [
            r"application received",
            r"under review",
            r"reviewing your application",
            r"we will get back",
            r"thank you for applying",
            r"currently reviewing"
        ]

    def classify(self, subject, body):

        text = f"{subject} {body}".lower()

        # ---------- Rule based classification ----------

        for pattern in self.selection_patterns:
            if re.search(pattern, text):
                return "Selection"

        for pattern in self.rejection_patterns:
            if re.search(pattern, text):
                return "Rejection"

        for pattern in self.pending_patterns:
            if re.search(pattern, text):
                return "Pending"

        # ---------- ML fallback ----------

        try:
            prediction = self.model.predict([text])[0]
            return prediction
        except Exception as e:
            print("ML classification failed:", e)
            return "Pending"