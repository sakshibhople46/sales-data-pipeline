import pandas as pd
from sqlalchemy import create_engine

def load_data(df: pd.DataFrame, db_path: str = "database/sales.db") -> None:
    """
    Load: Save the transformed DataFrame into a SQLite database.

    - Uses SQLAlchemy to connect to SQLite
    - Replaces the 'sales' table on every run (full refresh strategy)
    - Prints a confirmation with row count
    """
    try:
        engine = create_engine(f"sqlite:///{db_path}")

        df.to_sql(
            name="sales",
            con=engine,
            if_exists="replace",   # overwrite on each run
            index=False
        )

        print(f"[LOAD] Successfully loaded {len(df)} rows into '{db_path}' → table: sales")

    except Exception as e:
        raise RuntimeError(f"[LOAD] Failed to load data into database: {e}")