# Formula 1 Data Engineering Pipeline 🏎️💨

An end-to-end data pipeline built to ingest, clean, and model Formula 1 race performance data using data engineering concepts.

## 🛠️ Tech Stack & Tools
* Python: Used for data ingestion, processing, and executing raw ELT transformations.
* PostgreSQL: Serving as the local data warehouse to house raw structured and modeled tables.
* dbt (Data Build Tool): Utilized inside VS Code to build modular SQL data transformations, test data relationships, and compile models.
* Git/GitHub: For version control and deployment architecture tracking.

## 📐 Data Pipeline Architecture
1. Extraction & Ingestion: Custom Python script (`script/extraction_load.py`) pulls the analytical F1 records and writes them sequentially into our PostgreSQL staging database schema.
2. Staging Layer (`dbt_project/models/staging`): Actual transformation being performed and making models looks clean for each table and run generic schema tests (`unique`, `not_null`).
3. Mart Layer (`dbt_project/models/mart`): Serves as a final layer where dimension and fact table lives.