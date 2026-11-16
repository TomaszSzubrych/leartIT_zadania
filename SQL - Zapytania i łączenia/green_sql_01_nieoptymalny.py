import time
import pandas as pd

from green_sql_common import validate_database


def run(conn):
    query = """
    SELECT
        s.sale_id,
        s.sale_date,
        s.quantity,
        s.unit_price,
        c.region,
        p.category

    FROM sales s

    INNER JOIN customers c
        ON s.customer_id = c.customer_id

    INNER JOIN products p
        ON s.product_id = p.product_id
    """

    durations = []
    result = None

    for _ in range(3):
        start = time.perf_counter()

        # Pobranie wszystkich rekordów i filtrowanie w Pythonie
        df_all = pd.read_sql_query(query, conn)

        df_filtered = df_all[
            (df_all["region"] == "North")
            & (df_all["sale_date"] >= "2024-07-01")
        ].copy()

        df_filtered["revenue"] = (
            df_filtered["quantity"]
            * df_filtered["unit_price"]
        )

        result = (
            df_filtered
            .groupby("category", as_index=False)
            ["revenue"]
            .sum()
            .sort_values("revenue", ascending=False)
            .head(5)
            .reset_index(drop=True)
        )

        end = time.perf_counter()
        durations.append(end - start)

    plan = conn.execute(
        "EXPLAIN QUERY PLAN " + query
    ).fetchall()

    memory_bytes = int(
        df_all.memory_usage(deep=True).sum()
    )

    return {
        "name": "Nieoptymalny",
        "average_time": sum(durations) / 3,
        "memory_bytes": memory_bytes,
        "rows_fetched": len(df_all),
        "result": result,
        "plan": [row[3] for row in plan]
    }
