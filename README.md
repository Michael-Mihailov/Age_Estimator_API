# Age Estimator API

## Description

A project to provide stats on first name in the US from 1880-2024.

---

## Requirements

Install the required dependency:

```bash id="9kq2m1"
pip install sqlalchemy
```

---

## How to Run

### Build the Database

Run the following command to generate the SQLite database:

```bash id="4tq8ld"
python -m db.database_builder
```

This will create:

```text id="v2m9xa"
data/names.db
```
### Run the server

Run the following command:
```bash
python api/main_api.py
```
---

## Data Sources

This project uses data from the **Human Mortality Database (HMD)** and **Baby Names from Social Security Card Applications**.

* `data/life_tables`

**Citation:**

Human Mortality Database. Max Planck Institute for Demographic Research (Germany), University of California, Berkeley (USA), and French Institute for Demographic Studies (France).
Available at: https://www.mortality.org/  
  
Social Security Administration. Baby Names from Social Security Card Applications — National Data. Available at: https://catalog.data.gov/dataset/baby-names-from-social-security-card-applications-national-data

**License:**

The HMD data are licensed under the Creative Commons Attribution 4.0 International License (CC BY 4.0).  
The SSA Baby Names data are licensed under the Creative Commons Zero 1.0 Universal License (CC0 1.0).
