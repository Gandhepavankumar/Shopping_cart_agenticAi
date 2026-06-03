import os
import sqlite3
from langchain_core.tools import tool

DB_PATH = os.path.join(os.path.dirname(__file__), "store_db.db")


# @tool
def search_products(
    keyword: str = "",
    max_price: float | None = None,
    is_organic: bool | None = None
) -> list[dict]:
    """
    Search products by keyword and optionally filter by
    maximum price and organic status.
    """

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    sql_query = """
        SELECT id, name, description, price, is_organic
        FROM products
        WHERE 1=1
    """

    params = []

    if keyword:
        sql_query += " AND (name LIKE ? OR description LIKE ?)"
        like = f"%{keyword}%"
        params.extend([like, like])

    if max_price is not None:
        sql_query += " AND price <= ?"
        params.append(max_price)

    if is_organic is not None:
        sql_query += " AND is_organic = ?"
        params.append(1 if is_organic else 0)

    cursor.execute(sql_query, params)
    products = cursor.fetchall()

    conn.close()

    return [
        {
            "id": row[0],
            "name": row[1],
            "description": row[2],
            "price": row[3],
            "is_organic": bool(row[4]),
        }
        for row in products
    ]

if __name__ == "__main__":
    # Example usage
    results = search_products("apple", max_price=5.0, is_organic=True)
    print(results)