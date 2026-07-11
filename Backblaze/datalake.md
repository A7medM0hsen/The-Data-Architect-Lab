# 💾 Backblaze B2 Landing Zone & Data Lake Architecture

**Architectural Component:** Centralized Cloud Object Storage (Data Lake Landing Zone)  
**Data Scope:** Historical Aviation Flight Performance (Years 2024, 2025, 2026) + Metadata Dimensions  

---

## 📝 Layer Overview
This directory documents the Landing Zone / Data Lake layer of our enterprise data architecture. We utilize **Backblaze B2** as an immutable, highly durable cloud object storage repository. This layer isolates the extraction phase from downstream transformations, protecting our raw source assets and ensuring our pipeline remains completely decoupled.

All raw ingestion files are pushed directly from external web endpoints and local configurations into our target bucket (`airline-on-time-data-ahmed`) via automated python extraction scripts.

---

## 🗂️ Data Lake Storage Structure & Partitioning
The storage architecture inside Backblaze B2 is divided into two distinct processing paths: **Structured Partitioned Analytics Data** and **Semi-Structured Metadata Dimensions**.

```text
airline-on-time-data-ahmed/ (Bucket Root)
└── raw/
    ├── file1.json                   # Skytrax Airline Metadata Dimension
    ├── file2.json                   # OurAirports Airport Metadata Dimension
    └── flights/                     # Chronological Partitioned Flight Logs
        ├── year=2024/
        │   ├── month=01/flights_2024_01.zip
        │   ├── month=02/flights_2024_02.zip
        │   ├── month=03/flights_2024_03.zip
        │   ├── month=04/flights_2024_04.zip
        │   ├── month=05/flights_2024_05.zip
        │   ├── month=06/flights_2024_06.zip
        │   ├── month=07/flights_2024_07.zip
        │   ├── month=08/flights_2024_08.zip
        │   ├── month=09/flights_2024_09.zip
        │   ├── month=10/flights_2024_10.zip
        │   ├── month=11/flights_2024_11.zip
        │   └── month=12/flights_2024_12.zip
        ├── year=2025/
        │   ├── month=01/flights_2025_01.zip
        │   ├── month=02/flights_2025_02.zip
        │   ├── month=03/flights_2025_03.zip
        │   ├── month=04/flights_2025_04.zip
        │   ├── month=05/flights_2025_05.zip
        │   ├── month=06/flights_2025_06.zip
        │   ├── month=07/flights_2025_07.zip
        │   ├── month=08/flights_2025_08.zip
        │   ├── month=09/flights_2025_09.zip
        │   ├── month=10/flights_2025_10.zip
        │   ├── month=11/flights_2025_11.zip
        │   └── month=12/flights_2025_12.zip
        └── year=2026/
            ├── month=01/flights_2026_01.zip
            ├── month=02/flights_2026_02.zip
            ├── month=03/flights_2026_03.zip
            ├── month=04/flights_2026_04.zip
            └── month=05/flights_2026_05.zip
