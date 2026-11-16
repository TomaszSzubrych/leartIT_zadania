import time
import pandas as pd

from green_sql_common import create_indexes


def run(conn):
    create_indexes(conn)

    query = """
    SELECT
        p.category,
        SUM(s.quantity * s.unit_price) AS revenue

    FROM sales s

    INNER JOIN customers c
        ON s.customer_id = c.customer_id

    INNER JOIN products p
        ON s.product_id = p.product_id

    WHERE
        c.region = 'North'
        AND s.sale_date >= '2024-07-01'

    GROUP BY p.category

    ORDER BY revenue DESC

    LIMIT 5
    """

    durations = []
    result = None

    for _ in range(3):
        start = time.perf_counter()

        # Filtrowanie, agregacja i LIMIT w SQL
        result = pd.read_sql_query(
            query,
            conn
        )

        end = time.perf_counter()
        durations.append(end - start)

    plan = conn.execute(
        "EXPLAIN QUERY PLAN " + query
    ).fetchall()

    memory_bytes = int(
        result.memory_usage(deep=True).sum()
    )

    return {
        "name": "W pełni optymalny",
        "average_time": sum(durations) / 3,
        "memory_bytes": memory_bytes,
        "rows_fetched": len(result),
        "result": result,
        "plan": [row[3] for row in plan]
    }
