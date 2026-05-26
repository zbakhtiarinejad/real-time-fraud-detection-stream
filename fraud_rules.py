from datetime import datetime

recent_transactions = {}

MAX_AMOUNT = 5000
TIME_WINDOW = 300


def check_fraud(transaction):

    alerts = []

    card = transaction["card_number"]
    amount = transaction["amount"]
    country = transaction["country"]

    current_time = datetime.fromisoformat(transaction["timestamp"])

    # Rule 1 — Large Amount
    if amount > MAX_AMOUNT:
        alerts.append("Large transaction amount")

    # Rule 2 — Impossible Travel
    if card in recent_transactions:

        previous = recent_transactions[card]

        previous_country = previous["country"]
        previous_time = previous["timestamp"]

        time_difference = (current_time - previous_time).total_seconds()

        if previous_country != country and time_difference < TIME_WINDOW:
            alerts.append(
                f"Impossible travel ({previous_country} → {country})"
            )

    # Update latest activity
    recent_transactions[card] = {
        "country": country,
        "timestamp": current_time
    }

    return alerts