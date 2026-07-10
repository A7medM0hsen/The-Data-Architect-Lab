# 💾 Backblaze B2 Landing Zone & Data Lake Architecture

> **Architectural Component:** Centralized Cloud Object Storage (Data Lake Landing Zone)
> **Data Scope:** Historical Aviation Flight Performance (Years 2024, 2025, 2026) + Metadata Dimensions

---

## 📝 Layer Overview

This directory documents the **Landing Zone / Data Lake** layer of our enterprise data architecture. We utilize **Backblaze B2** as an immutable, highly durable cloud object storage repository. This layer isolates the extraction phase from downstream transformations, protecting our raw source assets and ensuring our pipeline remains completely decoupled.

All raw ingestion files are pushed directly from external web endpoints into our target bucket (`airline-on-time-data-ahmed`) via our automated extraction layer.

---

## 🗂️ Data Lake Storage Structure & Partitioning

The storage architecture inside Backblaze B2 is divided into two distinct processing paths: **Structured Partitioned Analytics Data** and **Semi-Structured Metadata Dimensions**.

### 1. Chronological Partitioned Flight Logs (Structured Layer)
The core transactional data consists of **29 heavily compressed `.zip` archives** containing multi-million row CSV logs extracted from the Bureau of Transportation Statistics (BTS). To minimize cloud compute execution times and structure the lake efficiently, data is stored using standard Hive partitioning standards:

```text
bucket/raw/flights/
├── 📂 year=2024/
│   ├── 📂 month=01/flights_2024_01.zip
│   ├── 📂 month=02/flights_2024_02.zip
│   └── [Rest of 2024 monthly compressed archives...]
├── 📂 year=2025/
│   ├── 📂 month=01/flights_2025_01.zip
│   └── [Rest of 2025 monthly compressed archives...]
└── 📂 year=2026/
    ├── 📂 month=01/flights_2026_01.zip
    └── [Rest of 2026 monthly compressed archives...]
