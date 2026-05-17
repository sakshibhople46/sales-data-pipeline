-- Schema reference for the sales table.
-- SQLAlchemy creates this automatically via df.to_sql(),
-- but this file documents the expected structure.

CREATE TABLE IF NOT EXISTS sales (
    order_id    INTEGER,
    product     TEXT,
    region      TEXT,
    sales_rep   TEXT,
    quantity    INTEGER,
    price       REAL,
    order_date  TEXT,
    revenue     REAL,
    month       TEXT
);