import pandas as pd

def extract_data(file_path: str) -> pd.DataFrame:
    """
    Extract: Read raw CSV data from disk.
    Validates that the file exists and loads it into a DataFrame.
    """
    try:
        df = pd.read_csv(file_path)
        print(f"[EXTRACT] Loaded {len(df)} rows from '{file_path}'")
        return df
    except FileNotFoundError:
        raise FileNotFoundError(f"[EXTRACT] File not found: {file_path}")
    except Exception as e:
        raise RuntimeError(f"[EXTRACT] Failed to read data: {e}")