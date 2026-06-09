CO_KEYWORDS = {

    "CO1": {

        "operating system": 3,
        "system call": 5,
        "system calls": 5,
        "os services": 5,
        "kernel": 4,
        "operating system services": 6,
        "operating system structure": 6,
        "operating system operations": 6
    },

    "CO2": {

        "process": 3,
        "process scheduling": 7,
        "fcfs": 8,
        "sjf": 8,
        "round robin": 8,
        "priority scheduling": 8,
        "scheduler": 7,
        "waiting time": 8,
        "turnaround time": 8,
        "gantt": 8,
        "cpu scheduling": 8
    },

    "CO3": {

        "critical section": 10,
        "peterson": 10,
        "mutex": 10,
        "semaphore": 10,
        "semaphores": 10,
        "deadlock": 10,
        "banker": 10,
        "safe state": 10,
        "need matrix": 10,
        "resource allocation": 8,
        "bounded buffer": 10,
        "reader writer": 10,
        "readers writers": 10,
        "synchronization": 10
    },

    "CO4": {

        "memory allocation": 10,
        "contiguous memory": 10,
        "paging": 10,
        "virtual memory": 10,
        "demand paging": 10,
        "page fault": 10,
        "page replacement": 10,
        "fifo": 10,
        "lru": 10,
        "optimal": 10,
        "segmentation": 10,
        "thrashing": 10,
        "logical address": 8,
        "physical address": 8,
        "tlb": 10
    },

    "CO5": {

        "file": 5,
        "file concept": 8,
        "file protection": 10,
        "file allocation": 10,
        "access method": 8,
        "disk scheduling": 10,
        "disk management": 10,
        "mass storage": 10,
        "protection": 8,
        "access matrix": 10,
        "domain of protection": 10
    }
}


def predict_co(question):

    q = question.lower()

    scores = {
        "CO1": 0,
        "CO2": 0,
        "CO3": 0,
        "CO4": 0,
        "CO5": 0
    }

    for co, keywords in CO_KEYWORDS.items():

        for keyword, weight in keywords.items():

            if keyword in q:
                scores[co] += weight

    best_co = max(scores, key=scores.get)

    if scores[best_co] == 0:
        return "CO1"

    return best_co


def co_confidence(question):

    q = question.lower()

    highest = 0

    for keywords in CO_KEYWORDS.values():

        for keyword, weight in keywords.items():

            if keyword in q:
                highest += weight

    confidence = min(60 + highest * 3, 99)

    return confidence


if __name__ == "__main__":

    while True:

        q = input("\nQuestion: ")

        print("CO:", predict_co(q))
        print("Confidence:", co_confidence(q), "%")