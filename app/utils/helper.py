def clean_sql(sql: str) -> str:
    # Remove markdown ```sql ```
    sql = sql.replace("```sql", "").replace("```", "")
    
    # Remove extra whitespace
    sql = sql.strip()
    
    return sql

def format_response(data):
    return {"count": len(data), "data": data}