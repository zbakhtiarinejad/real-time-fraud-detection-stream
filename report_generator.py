import pandas as pd
import os


def save_to_excel(transaction, alerts):

    file_name = "fraud_report.xlsx"

    data = {
        "Card Number": [transaction["card_number"]],
        "Amount": [transaction["amount"]],
        "Country": [transaction["country"]],
        "Timestamp": [transaction["timestamp"]],
        "Alerts": [", ".join(alerts)]
    }

    df = pd.DataFrame(data)

    # If file exists → append
    if os.path.exists(file_name):

        existing = pd.read_excel(file_name)

        updated = pd.concat([existing, df], ignore_index=True)

        updated.to_excel(file_name, index=False)

    else:
        df.to_excel(file_name, index=False)

    print("Fraud report updated.")