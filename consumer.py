import json
import time
import os
import pandas as pd

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet

from shared_queue import transaction_queue
from fraud_rules import check_fraud


# Store fraud alerts for PDF generation
fraud_alerts_data = []


# =========================
# EXCEL REPORT FUNCTION
# =========================

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

    # Append if file exists
    if os.path.exists(file_name):

        existing_df = pd.read_excel(file_name)

        updated_df = pd.concat(
            [existing_df, df],
            ignore_index=True
        )

        updated_df.to_excel(file_name, index=False)

    else:
        df.to_excel(file_name, index=False)

    print("Excel report updated.")


# =========================
# PDF REPORT FUNCTION
# =========================

def generate_pdf_report():

    pdf = SimpleDocTemplate("fraud_summary.pdf")

    styles = getSampleStyleSheet()

    content = []

    title = Paragraph(
        "Fraud Detection Summary Report",
        styles['Title']
    )

    content.append(title)

    content.append(Spacer(1, 20))

    for item in fraud_alerts_data:

        text = f"""
        <b>Card Number:</b> {item['card_number']}<br/>
        <b>Amount:</b> ${item['amount']}<br/>
        <b>Country:</b> {item['country']}<br/>
        <b>Timestamp:</b> {item['timestamp']}<br/>
        <b>Alerts:</b> {item['alerts']}<br/><br/>
        """

        paragraph = Paragraph(
            text,
            styles['BodyText']
        )

        content.append(paragraph)

        content.append(Spacer(1, 12))

    pdf.build(content)

    print("PDF report generated.")


# =========================
# CONSUMER FUNCTION
# =========================

def start_consumer():

    print("Consumer started...\n")

    while True:

        if not transaction_queue.empty():

            transaction = transaction_queue.get()

            alerts = check_fraud(transaction)

            print("=" * 60)

            print(f"Card Number : {transaction['card_number']}")
            print(f"Amount      : ${transaction['amount']}")
            print(f"Country     : {transaction['country']}")
            print(f"Timestamp   : {transaction['timestamp']}")

            # =========================
            # FRAUD DETECTED
            # =========================

            if alerts:

                print("\nFRAUD ALERT DETECTED")

                for alert in alerts:
                    print(f"-> {alert}")

                # Save JSON log
                with open("fraud_log.json", "a") as file:
                    file.write(json.dumps(transaction) + "\n")

                # Save Excel report
                save_to_excel(transaction, alerts)

                # Store data for PDF
                fraud_alerts_data.append({
                    "card_number": transaction["card_number"],
                    "amount": transaction["amount"],
                    "country": transaction["country"],
                    "timestamp": transaction["timestamp"],
                    "alerts": ", ".join(alerts)
                })

                # Generate PDF report
                generate_pdf_report()

            # =========================
            # NORMAL TRANSACTION
            # =========================

            else:
                print("\nTransaction Normal")

            print("=" * 60)

        time.sleep(0.5)