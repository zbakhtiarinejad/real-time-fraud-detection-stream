# Real-Time Fraud Detection Stream

A real-time fraud detection simulation built with Python using a producer-consumer streaming architecture.

This project simulates live banking transactions, analyzes them instantly using fraud detection rules, and automatically generates fraud reports in Excel and PDF format.

---

# Features

- Real-time transaction streaming
- Producer-consumer architecture
- Fraud detection engine
- Large transaction detection
- Impossible travel detection
- Automated Excel reporting
- Automated PDF reporting
- JSON fraud logging

---

# Fraud Detection Rules

## Rule 1 — Large Transaction

Flags transactions with amounts greater than $5000.

## Rule 2 — Impossible Travel

Flags transactions when the same card is used in two different countries within 5 minutes.

---

# Architecture

```text
Transaction Generator
        ↓
Shared Queue
        ↓
Consumer Processor
        ↓
Fraud Detection Engine
        ↓
Excel / PDF Reports
```

---

# Technologies Used

- Python
- Threading
- Queue
- Pandas
- OpenPyXL
- ReportLab

---

# Project Structure

```text
fraud-detection-stream/
│
├── producer.py
├── consumer.py
├── fraud_rules.py
├── shared_queue.py
├── main.py
├── fraud_log.json
├── fraud_report.xlsx
├── fraud_summary.pdf
└── README.md
```

---

# How to Run

## Install dependencies

```bash
pip install pandas openpyxl reportlab
```

## Run the project

```bash
python main.py
```

---

# Output

The system automatically:

- Generates live transactions
- Detects suspicious activity
- Logs fraud events
- Creates Excel reports
- Generates PDF summaries
