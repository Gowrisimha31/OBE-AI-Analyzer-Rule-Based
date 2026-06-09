import joblib
import os

# Load models lazily to avoid import-time crashes when model files are missing
MODEL_PATH = "models/bloom_model.pkl"
VECT_PATH = "models/bloom_vectorizer.pkl"

model = None
vectorizer = None
_models_loaded = False

def _load_models():
    global model, vectorizer, _models_loaded
    if _models_loaded:
        return
    _models_loaded = True
    try:
        if os.path.exists(MODEL_PATH) and os.path.exists(VECT_PATH):
            model = joblib.load(MODEL_PATH)
            vectorizer = joblib.load(VECT_PATH)
    except Exception:
        model = None
        vectorizer = None

BLOOM_LEVELS = {
    "Remember": 1,
    "Understand": 2,
    "Apply": 3,
    "Analyze": 4,
    "Evaluate": 5,
    "Create": 6
}

BLOOM_RULES = {

    "Remember": [
        "define", "list", "name", "identify",
        "state", "recall", "mention",
        "label", "recognize", "select",
        "match", "locate"
    ],

    "Understand": [
        "explain", "describe", "discuss",
        "summarize", "illustrate",
        "classify", "interpret",
        "outline", "clarify",
        "review"
    ],

    "Apply": [
        "apply", "calculate", "compute",
        "solve", "demonstrate",
        "implement", "use",
        "draw", "execute",
        "perform"
    ],

    "Analyze": [
        "analyze", "compare",
        "differentiate",
        "distinguish",
        "examine", "contrast",
        "investigate", "inspect"
    ],

    "Evaluate": [
        "evaluate", "justify",
        "assess", "recommend",
        "critique", "judge",
        "validate", "verify"
    ],

    "Create": [
        "design", "develop",
        "construct", "create",
        "propose", "formulate",
        "build", "generate",
        "invent", "plan"
    ]
}


def predict_bloom(question):

    q = question.lower()

    detected_levels = []

    for level, verbs in BLOOM_RULES.items():

        for verb in verbs:

            if verb in q:
                detected_levels.append(level)

    if detected_levels:

        return max(
            detected_levels,
            key=lambda x: BLOOM_LEVELS[x]
        )

    # Attempt to use trained model if available. If model files are missing
    # fall back to rule-based detection (above) or a safe default.
    _load_models()

    if model is None or vectorizer is None:
        return "Remember"

    vec = vectorizer.transform([question])

    prediction = model.predict(vec)[0]

    return prediction


def bloom_confidence(question):

    q = question.lower()

    matches = 0

    for verbs in BLOOM_RULES.values():

        for verb in verbs:

            if verb in q:
                matches += 1

    confidence = min(70 + matches * 10, 99)

    return confidence


if __name__ == "__main__":

    while True:

        q = input("\nQuestion: ")

        print("Bloom:", predict_bloom(q))
        print("Confidence:", bloom_confidence(q), "%")