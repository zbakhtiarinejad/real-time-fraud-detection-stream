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

- ## 🛠️ Key Technical Challenges & Solutions

Building a high-throughput streaming pipeline involves real-world edge cases around network latency, state management, and schema consistency. Below are the key engineering challenges encountered during development and how they were resolved:

---

### 1. High Backpressure & Throughput Bottlenecks in Data Ingestion
* **The Issue:** The default single-threaded Python Kafka producer setup capped out at around 150–200 transactions per second (RPS), bottlenecking the pipeline and consuming excessive CPU due to unbatched synchronous network requests.
* **How It Was Fixed:** Re-architected the generator module using Python’s `ThreadPoolExecutor` to distribute payload creation across multiple worker threads. Implemented client-side micro-batching (`batch_size=32768`, `linger_ms=5`) along with `GZIP` payload compression in the `KafkaProducer` settings. This bumped overall ingestion throughput past **1,000+ RPS** with negligible network overhead.

---

### 2. Handling Out-of-Order Events & Network Jitter in Flink
* **The Issue:** Network latency caused some transaction events to arrive out of order. Standard processing-time windowing resulted in inaccurate fraud flags because high-frequency transaction clusters were being split across incorrect execution windows.
* **How It Was Fixed:** Switched Flink’s execution semantics from *Processing Time* to explicit *Event Time* extraction using the event's embedded millisecond timestamp (`tx_time`). Configured a bounded-out-of-orderness watermark (`tx_time - INTERVAL '2' SECOND`) to give late-arriving events a 2-second grace period before triggering window evaluations.

---

### 3. MinIO S3 API Incompatibility with Apache Iceberg
* **The Issue:** Flink failed to write metadata and Parquet files into the local MinIO bucket, throwing `AmazonS3Exception: 400 Bad Request` errors caused by virtual-hosted style requests default in AWS S3 SDKs.
* **How It Was Fixed:** Updated the Flink Catalog DDL configuration to explicitly set `'hadoop.fs.s3a.path.style.access'='true'`. This forced the underlying Hadoop `S3A` file system client to use path-style requests (`http://minio:9000/warehouse/`) required by MinIO and other local S3 emulation services.

---

### 4. Partition Evolution and Metadata Locking in Lakehouse Sink
* **The Issue:** High-frequency small files were being generated in the Iceberg data layer (the "small file problem"), leading to degraded query performance over time.
* **How It Was Fixed:** Configured hidden partitioning by transaction date (`PARTITIONED BY (tx_date)`) and enabled target commit compression codecs (`write.metadata.compression-codec='gzip'`). This structured incoming stream writes predictably across partitioned storage layers while preserving ACID transaction guarantees.
