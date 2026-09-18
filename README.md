# Formula 1 Data Engineering Pipeline 🏎️💨

An end-to-end data pipeline built to ingest, clean, and model historical Formula 1 race performance datasets using data engineering best practices.

## 🛠️ Tech Stack & Tools
* Python: Used for data ingestion, processing, and executing raw ETL transformations.
* PostgreSQL: Serving as the centralized local data warehouse to house raw structured and modeled tables.
* dbt (Data Build Tool): Utilized inside VS Code to build modular SQL data transformations, test data relationships, and compile models.
* Git/GitHub: For version control and deployment architecture tracking.

## 📐 Data Pipeline Architecture
1. Extraction & Ingestion: Custom Python script (`script/extraction_load.py`) pulls the analytical F1 records and writes them sequentially into our PostgreSQL staging database schema.
2. Staging Layer (`stg_`): Standardized schema models are generated using dbt to clean data types, ensure data integrity, and run generic schema tests (`unique`, `not_null`).
3. Data Quality Framework: Automated data quality tests are actively maintained via our configurations to enforce primary key uniqueness and schema relationship mappings across the tables.