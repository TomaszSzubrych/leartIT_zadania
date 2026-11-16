import sqlite3
import numpy as np


NUMBER_OF_SALES = 500_000
NUMBER_OF_CUSTOMERS = 20_000
NUMBER_OF_PRODUCTS = 100


def build_database():
    rng = np.random.default_rng(42)

    regions = np.array([
        "North", "South", "East", "West"
    ])

    categories = np.array([
        "Elektronika",
        "Meble",
        "Akcesoria",
        "Odziez",
        "Sport"
    ])

    customers = [
        (i + 1, str(regions[i % len(regions)]))
        for i in range(NUMBER_OF_CUSTOMERS)
    ]

    products = [
        (i + 1, str(categories[i % len(categories)]))
        for i in range(NUMBER_OF_PRODUCTS)
    ]

    customer_ids = rng.integers(
        1, NUMBER_OF_CUSTOMERS + 1,
        size=NUMBER_OF_SALES
    )

    product_ids = rng.integers(
        1, NUMBER_OF_PRODUCTS + 1,
        size=NUMBER_OF_SALES
    )

    quantities = rng.integers(
        1, 11,
        size=NUMBER_OF_SALES
    )

    prices = np.round(
        rng.uniform(20, 2000, size=NUMBER_OF_SALES),
        2
    )

    date_offsets = rng.integers(
        0, 366,
        size=NUMBER_OF_SALES
    )

    dates = (
        np.datetime64("2024-01-01")
        + date_offsets.astype("timedelta64[D]")
    )

    sales = [
        (
            i + 1,
            int(customer_ids[i]),
            int(product_ids[i]),
            int(quantities[i]),
            float(prices[i]),
            str(dates[i])
        )
        for i in range(NUMBER_OF_SALES)
    ]

    conn = sqlite3.connect(":memory:")

    conn.execute("""
    CREATE TABLE customers (
        customer_id INTEGER PRIMARY KEY,
        region TEXT NOT NULL
    )
    """)

    conn.execute("""
    CREATE TABLE products (
        product_id INTEGER PRIMARY KEY,
        category TEXT NOT NULL
    )
    """)

    conn.execute("""
    CREATE TABLE sales (
        sale_id INTEGER PRIMARY KEY,
        customer_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        unit_price REAL NOT NULL,
        sale_date TEXT NOT NULL,
        FOREIGN KEY (customer_id)
            REFERENCES customers(customer_id),
        FOREIGN KEY (product_id)
            REFERENCES products(product_id)
    )
    """)

    conn.executemany("""
    INSERT INTO customers (customer_id, region)
    VALUES (?, ?)
    """, customers)

    conn.executemany("""
    INSERT INTO products (product_id, category)
    VALUES (?, ?)
    """, products)

    conn.executemany("""
    INSERT INTO sales (
        sale_id,
        customer_id,
        product_id,
        quantity,
        unit_price,
        sale_date
    )
    VALUES (?, ?, ?, ?, ?, ?)
    """, sales)

    conn.commit()

    return conn


def create_indexes(conn):
    conn.execute("""
    CREATE INDEX idx_customers_region
    ON customers(region)
    """)

    conn.execute("""
    CREATE INDEX idx_sales_customer
    ON sales(customer_id)
    """)

    conn.execute("""
    CREATE INDEX idx_sales_date
    ON sales(sale_date)
    """)

    conn.execute("ANALYZE")
    conn.commit()


def validate_database(conn):
    count = conn.execute(
        "SELECT COUNT(*) FROM sales"
    ).fetchone()[0]

    if count != NUMBER_OF_SALES:
        raise ValueError(
            f"Oczekiwano {NUMBER_OF_SALES} transakcji, otrzymano {count}."
        )

    return count
