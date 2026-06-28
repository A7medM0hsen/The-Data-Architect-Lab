# The-Data-Architect-Lab
"A collaborative environment for building and testing modern data engineering pipelines and end-to-end solutions.


# ✈️ US Airline Data Engineering Pipeline (End-to-End ELT)

An enterprise-grade data engineering pipeline designed to ingest, transform, and orchestrate over **14 Million rows** of historical US flight data for the years **2024 and 2025**. 

The project follows the **ELT (Extract, Load, Transform)** pattern, leveraging **Snowflake** and **Snowpark (Python)** for scalable ingestion, **dbt** for modular analytics engineering, and **Apache Airflow** for workflow orchestration.

---

## 🏗️ Project Architecture & Workflow

1. **Extract & Load (EL):** Raw multi-volume `.zip` files containing monthly flight data are uploaded to a Snowflake Internal Stage.
2. **Ingestion Engine (Snowpark Python):** A robust stored procedure unzips, processes, and structures data on the fly using Python & Pandas directly inside Snowflake compute clusters.
3. **Orchestrated Bulk Loading:** A dynamic SQL Loop identifies the file metadata (target year) from the file name, handles authentication via Scoped URLs, and bulk-loads 24 months of data into raw tables.
4. **Transformation (T) - *[Current Phase]*:** Data transformation, type casting, quality validation, and star-schema dimensional modeling using **dbt**.
5. **Orchestration:** Pipeline automation and scheduling handled by **Apache Airflow**.

---

## 📊 Current Ingestion Metrics (Raw Layer)

The Ingestion layer completed running successfully in **9 minutes and 11 seconds**, inserting **14,080,680 records** into the database completely free of errors:

* **Database:** `AIRLINE_DB`
* **Schema:** `RAW`
* **Tables Created:**
  * `RAW_FLIGHTS_2024`: **7,079,061** Rows (Optimized Columnar Storage Size: ~288.4 MB)
  * `RAW_FLIGHTS_2025`: **7,001,619** Rows (Optimized Columnar Storage Size: ~281.7 MB)

---

## 🛠️ Key Engineering Challenges Solved (Ingestion Layer)

### 💥 The "SLC Airport Code" Schema Drift Bug
* **The Problem:** Flight data contains highly sparse diversion columns (e.g., `Div1Airport`). In early months (e.g., January 2024), these columns were 100% empty, causing Pandas and Snowflake to infer the datatype as `REAL` (Float). In later months, string data suddenly appeared (e.g., airport code `"SLC"`), breaking the copy pipeline with a `Failed to cast variant value "SLC" to FIXED/REAL` error.
* **The Engineering Solution:** Implemented an **Ingestion Bulletproofing Strategy**. Modified the Snowpark script to read all raw columns explicitly as `dtype=str` (`VARCHAR`) and mapped missing values (`NaN`) to explicit empty strings `''`. This strategy guarantees that the ingestion pipeline never breaks due to dirty raw data, separating the concerns by deferring all type-casting and parsing to the **dbt transformation layer**.

---

## 🚀 Next Steps for Collaborators (dbt Layer)

Welcome to the team! Since the raw ingestion layer is successfully deployed, your role is to build the transformation models. Please follow these guidelines:

1. **Snowflake Connection:** Connect your local dbt project or dbt Cloud instance using the database `AIRLINE_DB`, warehouse `COMPUTE_WH`, and role `ACCOUNTADMIN`.
2. **Staging Layer Transformations:**
   * **Data Cleansing:** Convert raw empty string tokens `''` back to true `NULL` values using conditional logic: `CASE WHEN column = '' THEN NULL ELSE column END`.
   * **Type Casting:** Cast the raw text columns into their appropriate analytical types (e.g., convert text dates to `DATE`, delay metrics to `INT`, and coordinates to `FLOAT`).
3. **Marts Layer:** Design the dimensional modeling structure (Fact and Dimension tables) to produce a clean star schema optimized for BI dashboard ingestion.

---
*Note: The Snowflake Virtual Warehouse (`COMPUTE_WH`) is configured with `AUTO_SUSPEND = 60` and `AUTO_RESUME = TRUE` to optimize cloud credit consumption. It will automatically spin up whenever you execute a dbt run.*
