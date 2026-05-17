# 📊 SalesIQ — Sales Analytics Pipeline & Dashboard

An end-to-end data engineering project featuring a Python ETL pipeline, SQLite data warehouse, and an interactive Streamlit dashboard with Plotly visualisations.

---

## 🗂 Project Structure

```
salesiq/
├── dashboard/
│   ├── __init__.py
│   └── app.py              # Streamlit dashboard (KPIs, charts, filters, export)
├── data/
│   ├── __init__.py
│   ├── generate_data.py    # Synthetic data generation via Faker
│   └── raw_sales.csv       # Generated raw data (500 rows)
├── database/
│   ├── sales.db            # SQLite database (auto-created by pipeline)
│   └── schema.sql          # Table schema reference
├── etl/
│   ├── __init__.py
│   ├── extract.py          # Read CSV into DataFrame
│   ├── transform.py        # Clean, dedupe, enrich data
│   └── load.py             # Write to SQLite via SQLAlchemy
├── queries/
│   ├── __init__.py
│   └── analytics.py        # Reusable SQL query helpers
├── run_pipeline.py         # Orchestrates the full ETL run
├── requirements.txt
└── README.md
```

---

## ⚙️ How It Works

### 1. Data Generation
`generate_data.py` uses the **Faker** library to produce 500 synthetic sales records with realistic noise — duplicate order IDs, missing sales reps, and negative quantities — simulating real-world messy data.

**Fields generated:** `order_id`, `product`, `region`, `sales_rep`, `quantity`, `price`, `order_date`

### 2. ETL Pipeline

The pipeline runs in three clean, modular stages:

| Stage | File | What it does |
|---|---|---|
| **Extract** | `etl/extract.py` | Reads `raw_sales.csv` into a pandas DataFrame |
| **Transform** | `etl/transform.py` | Deduplicates on `order_id`, drops null `sales_rep`, removes zero/negative `quantity`, computes `revenue = quantity × price`, parses dates, adds `month` column |
| **Load** | `etl/load.py` | Writes cleaned DataFrame to `sales` table in SQLite via SQLAlchemy (`if_exists="replace"`) |

Run the full pipeline:
```bash
python run_pipeline.py
```

### 3. Streamlit Dashboard
`dashboard/app.py` reads directly from `sales.db` and provides:

- **Sidebar filters** — by product, region, and sales rep
- **KPI cards** — Total Revenue, Total Orders, Avg Order Value, Top Sales Rep
- **6 interactive Plotly charts:**
  - Revenue by Product (horizontal bar)
  - Revenue by Region (donut)
  - Monthly Revenue Trend (area line)
  - Sales Rep Leaderboard (bar)
  - Order Volume by Product (bar)
  - Region × Product Revenue Heatmap
- **Filterable data table** with formatted ₹ values
- **CSV export** of the filtered view

Launch the dashboard:
```bash
streamlit run dashboard/app.py
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/salesiq.git
cd salesiq

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Generate data and run the ETL pipeline
python data/generate_data.py
python run_pipeline.py

# Launch the dashboard
streamlit run dashboard/app.py
```

---

## 🛠 Tech Stack

| Tool | Role |
|---|---|
| **Python 3** | Core language |
| **Pandas** | Data manipulation in the ETL pipeline |
| **Faker** | Synthetic data generation |
| **SQLAlchemy** | ORM / database connection layer |
| **SQLite** | Lightweight local data warehouse |
| **Streamlit** | Web dashboard framework |
| **Plotly** | Interactive charts and heatmaps |

---

## 📈 Key Concepts Demonstrated

- **ETL pipeline design** with separation of concerns (extract / transform / load)
- **Data cleaning** — deduplication, null handling, outlier removal
- **Feature engineering** — revenue calculation, date parsing, month extraction
- **Relational database** storage with a defined schema
- **Interactive data visualisation** with drill-down filtering
- **Modular Python project structure** with reusable query helpers

---
