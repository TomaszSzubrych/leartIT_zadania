import time
import pandas as pd

from green_sql_common import create_indexes


def run(conn):
    create_indexes(conn)

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

    WHERE
        c.region = 'North'
        AND s.sale_date >= '2024-07-01'
    """

    durations = []
    result = None

    for _ in range(3):
        start = time.perf_counter()

        # Filtrowanie w SQL, agregacja w Pythonie
        df_filtered = pd.read_sql_query(
            query,
            conn
        )

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
        df_filtered.memory_usage(deep=True).sum()
    )

    return {
        "name": "Częściowo optymalny",
        "average_time": sum(durations) / 3,
        "memory_bytes": memory_bytes,
        "rows_fetched": len(df_filtered),
        "result": result,
        "plan": [row[3] for row in plan]
    }
