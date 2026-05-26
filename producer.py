import random
import time
from datetime import datetime
from shared_queue import transaction_queue


cards = [
    "4532123412341234",
    "4532987612345678",
    "5123412398761111",
    "6011123412349999",
    "4000123412345555"
]

countries = [
    "USA",
    "Germany",
    "Japan",
    "Canada",
    "France",
    "Brazil",
    "UAE"
]


def start_producer():

    print("Streaming transactions...\n")

    while True:

        transaction = {
            "card_number": random.choice(cards),
            "amount": random.randint(10, 10000),
            "country": random.choice(countries),
            "timestamp": datetime.now().isoformat()
        }

        transaction_queue.put(transaction)

        print(f"Produced: {transaction}")

        time.sleep(1)