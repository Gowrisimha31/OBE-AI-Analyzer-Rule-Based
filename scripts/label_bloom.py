import pandas as pd

# Load master questions
df = pd.read_csv("dataset/master_questions.csv")


def label_bloom(question):

    words = str(question).lower().split()

    remember = [
        "define", "list", "name", "identify",
        "state", "recall", "mention", "label",
        "recognize", "select", "match", "locate"
    ]

    understand = [
        "explain", "describe", "discuss",
        "summarize", "illustrate", "classify",
        "interpret", "outline", "clarify",
        "express", "review"
    ]

    apply = [
        "apply", "calculate", "compute",
        "solve", "demonstrate", "implement",
        "use", "draw", "execute",
        "perform", "show", "operate"
    ]

    analyze = [
        "analyze", "compare", "differentiate",
        "distinguish", "examine",
        "contrast", "investigate",
        "categorize", "inspect",
        "infer", "test"
    ]

    evaluate = [
        "evaluate", "justify", "assess",
        "recommend", "critique",
        "judge", "validate",
        "verify", "argue", "defend"
    ]

    create = [
        "design", "develop", "construct",
        "create", "propose", "formulate",
        "build", "generate",
        "plan", "invent", "compose"
    ]

    # Check Create first
    for word in create:
        if word in words:
            return "Create"

    # Check Evaluate
    for word in evaluate:
        if word in words:
            return "Evaluate"

    # Check Analyze
    for word in analyze:
        if word in words:
            return "Analyze"

    # Check Apply
    for word in apply:
        if word in words:
            return "Apply"

    # Check Understand
    for word in understand:
        if word in words:
            return "Understand"

    # Check Remember
    for word in remember:
        if word in words:
            return "Remember"

    # If no Bloom verb found
    return "Unknown"


# Label questions
df["bloom_level"] = df["question"].apply(label_bloom)

df = df[df["bloom_level"] != "Unknown"]

# Save dataset
df.to_csv(
    "dataset/bloom_dataset.csv",
    index=False
)

# Show counts
print(df["bloom_level"].value_counts())