import pandas as pd

def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transform: Clean and enrich the raw sales data.

    Steps:
      1. Drop duplicate order_ids
      2. Drop rows where sales_rep is missing
      3. Remove rows with negative or zero quantity
      4. Calculate revenue = quantity * price
      5. Convert order_date to datetime
      6. Add a month column for time-based analysis
    """

    print(f"[TRANSFORM] Starting with {len(df)} rows")

    # 1. Remove duplicate orders
    df = df.drop_duplicates(subset=["order_id"])
    print(f"[TRANSFORM] After dropping duplicates: {len(df)} rows")

    # 2. Drop rows with missing sales_rep
    df = df.dropna(subset=["sales_rep"])
    print(f"[TRANSFORM] After dropping missing sales_rep: {len(df)} rows")

    # 3. Remove invalid quantities (negative or zero)
    df = df[df["quantity"] > 0]
    print(f"[TRANSFORM] After removing invalid quantities: {len(df)} rows")

    # 4. Calculate revenue
    df = df.copy()  # avoid SettingWithCopyWarning
    df["revenue"] = df["quantity"] * df["price"]

    # 5. Parse order_date
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")

    # 6. Add month column
    df["month"] = df["order_date"].dt.to_period("M").astype(str)

    print(f"[TRANSFORM] Transformation complete. Final rows: {len(df)}")
    return df