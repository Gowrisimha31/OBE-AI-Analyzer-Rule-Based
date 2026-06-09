from scripts.predict_co import predict_co


PO_MAPPING = {

    "CO1": ["PO1", "PO2"],

    "CO2": ["PO2", "PO3"],

    "CO3": ["PO1", "PO3", "PO4"],

    "CO4": ["PO4", "PO5"],

    "CO5": ["PO3", "PO5"]
}


def predict_po(question):

    co = predict_co(question)

    return PO_MAPPING.get(co, [])


if __name__ == "__main__":

    while True:

        question = input("\nEnter Question: ")

        po = predict_po(question)

        print("Mapped POs:", po)