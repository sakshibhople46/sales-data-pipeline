import pandas as pd
from sqlalchemy import create_engine

# ---------------------------------------------------------------------------
# These helper functions query the SQLite database and return DataFrames.
# They are imported by app.py but the actual filtering/aggregation in the
# dashboard is done directly on the in-memory filtered_df for speed.
# Use these for standalone scripts or scheduled reports.
# ---------------------------------------------------------------------------

def get_engine(db_path: str = "database/sales.db"):
    return create_engine(f"sqlite:///{db_path}")


def total_revenue(engine=None) -> float:
    """Return total revenue across all records."""
    if engine is None:
        engine = get_engine()
    df = pd.read_sql("SELECT SUM(revenue) as total FROM sales", engine)
    return df["total"].iloc[0] or 0.0


def top_products(engine=None, n: int = 5) -> pd.DataFrame:
    """Return top N products by total revenue."""
    if engine is None:
        engine = get_engine()
    query = """
        SELECT product, SUM(revenue) as total_revenue
        FROM sales
        GROUP BY product
        ORDER BY total_revenue DESC
        LIMIT :n
    """
    return pd.read_sql(query, engine, params={"n": n})


def region_sales(engine=None) -> pd.DataFrame:
    """Return total revenue grouped by region."""
    if engine is None:
        engine = get_engine()
    query = """
        SELECT region, SUM(revenue) as total_revenue
        FROM sales
        GROUP BY region
        ORDER BY total_revenue DESC
    """
    return pd.read_sql(query, engine)