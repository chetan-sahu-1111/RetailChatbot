BLOCKED_KEYWORDS = ["drop", "delete", "update", "insert", "alter"]

VALID_TABLES = ["products", "orders", "order_items", "customers"]

def is_safe_query(sql: str):
    sql_lower = sql.lower()
    return not any(word in sql_lower for word in BLOCKED_KEYWORDS)


def uses_valid_tables(sql: str):
    sql_lower = sql.lower()
    return any(table in sql_lower for table in VALID_TABLES)


def add_limit(sql: str):
    if "limit" not in sql.lower():
        return sql.strip().rstrip(";") + " LIMIT 100;"
    return sql

def validate_result(result):
    if result is None:
        return False
    if isinstance(result, list) and len(result) == 0:
        return False
    return True