# Age Estimator API

## Description

A project to estimate a person's age using their first name.

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
python db/database_builder.py
```

This will create:

```text id="v2m9xa"
data/names.db
```

---

## Data Sources

This project uses data from the **Human Mortality Database (HMD)**:

* `data/life_tables`

**Citation:**

Human Mortality Database. Max Planck Institute for Demographic Research (Germany), University of California, Berkeley (USA), and French Institute for Demographic Studies (France).
Available at: https://www.mortality.org/

**License:**

The HMD data are licensed under the Creative Commons Attribution 4.0 International License (CC BY 4.0).
