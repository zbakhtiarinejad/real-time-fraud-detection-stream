import json
import os
import pandas as pd
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

from fraud_rules import check_fraud
from shared_queue import transaction_queue

EXCEL_FILE = "fraud_report.xlsx"
PDF_FILE = "fraud_summary.pdf"
JSON_LOG = "fraud_log.json"

fraud_alerts_data = []


def append_to_excel(transaction: dict, alerts: list[str]) -> None:
    """Appends a new fraud record to the Excel report."""
    record = {
        "Card Number": [transaction["card_number"]],
        "Amount": [transaction["amount"]],
        "Country": [transaction["country"]],
        "Timestamp": [transaction["timestamp"]],
        "Alerts": [", ".join(alerts)],
    }
    new_df = pd.DataFrame(record)

    if os.path.exists(EXCEL_FILE):
        existing_df = pd.read_excel(EXCEL_FILE)
        updated_df = pd.concat([existing_df, new_df], ignore_index=True)
        updated_df.to_excel(EXCEL_FILE, index=False)
    else:
        new_df.to_excel(EXCEL_FILE, index=False)


def generate_pdf_report(records: list[dict]) -> None:
    """Generates a summary PDF report from accumulated fraud records."""
    pdf = SimpleDocTemplate(PDF_FILE)
    styles = getSampleStyleSheet()
    story = [
        Paragraph("Fraud Detection Summary Report", styles["Title"]),
        Spacer(1, 20),
    ]

    for item in records:
        text = (
            f"<b>Card Number:</b> {item['card_number']}<br/>"
            f"<b>Amount:</b> ${item['amount']}<br/>"
            f"<b>Country:</b> {item['country']}<br/>"
            f"<b>Timestamp:</b> {item['timestamp']}<br/>"
            f"<b>Alerts:</b> {item['alerts']}<br/><br/>"
        )
        story.extend([Paragraph(text, styles["BodyText"]), Spacer(1, 12)])

    pdf.build(story)


def process_transaction(transaction: dict) -> None:
    """Evaluates a single transaction and handles logging/reporting if flagged."""
    alerts = check_fraud(transaction)

    print("=" * 60)
    print(f"Card Number : {transaction['card_number']}")
    print(f"Amount      : ${transaction['amount']}")
    print(f"Country     : {transaction['country']}")
    print(f"Timestamp   : {transaction['timestamp']}")

    if not alerts:
        print("\nStatus: Normal")
        print("=" * 60)
        return

    print("\nFRAUD ALERT DETECTED:")
    for alert in alerts:
        print(f"  -> {alert}")
    print("=" * 60)

    # 1. Append JSON log
    with open(JSON_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(transaction) + "\n")

    # 2. Append Excel record
    append_to_excel(transaction, alerts)

    # 3. Update PDF report
    fraud_record = {**transaction, "alerts": ", ".join(alerts)}
    fraud_alerts_data.append(fraud_record)
    generate_pdf_report(fraud_alerts_data)


def start_consumer() -> None:
    """Main event loop consuming from the shared queue."""
    print("Consumer started processing queue...\n")
    while True:
        # Blocking get prevents CPU spinning and removes need for manual sleep
        transaction = transaction_queue.get(block=True)
        process_transaction(transaction)
