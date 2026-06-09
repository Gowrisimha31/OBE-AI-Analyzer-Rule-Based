from scripts.predict_bloom import predict_bloom
from scripts.predict_co import predict_co
from scripts.predict_po import predict_po

while True:

    question = input("\nEnter Question: ")

    bloom = predict_bloom(question)
    co = predict_co(question)
    po = predict_po(question)

    print("\nBloom Level:", bloom)
    print("Course Outcome:", co)
    print("Program Outcomes:", ", ".join(po))