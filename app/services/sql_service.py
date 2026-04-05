from app.services.llm_service import call_llm

SCHEMA = """
Tables:
products(id, name, price, stock)
orders(id, date, total_amount)
order_items(id, order_id, product_id, quantity)
"""

def generate_sql(user_query: str):
    prompt = prompt = f"""
You are an expert MySQL query generator.

Your task is to convert a natural language question into a syntactically correct and executable SQL query.

=====================
DATABASE SCHEMA: {SCHEMA}
=====================

=====================
STRICT RULES:
=====================
1. ONLY generate a valid MySQL SELECT query.
2. DO NOT generate INSERT, UPDATE, DELETE, DROP, ALTER, TRUNCATE.
3. DO NOT include any explanation.
4. DO NOT include markdown (NO ```sql or ```).
5. DO NOT include comments.
6. Output must be plain SQL text only.
7. Ensure correct table joins using foreign keys:
   - orders.customer_id → customers.id
   - order_items.order_id → orders.id
   - order_items.product_id → products.id
8. Use proper aliases (p, o, oi, c) for readability.
9. Always handle aggregations properly:
   - Use GROUP BY when using SUM, COUNT, AVG
10. Use ORDER BY when user asks for "top", "highest", "lowest"
11. Use LIMIT when user asks for "top N"
12. Handle NULL values safely if needed (use COALESCE if required)
13. Use correct date filtering for queries involving time
14. Avoid ambiguous column names (always prefix with table alias)
15. Ensure SQL is executable in MySQL without modification
16. Do NOT end query with semicolon (;)

=====================
EDGE CASE HANDLING:
=====================
- If question is ambiguous, assume most logical business meaning
- If asking for "revenue", calculate using:
  SUM(order_items.quantity * products.price)
- If asking for "sales", use orders.total_amount or derived revenue
- If asking for "top selling", sort by total quantity sold
- If asking for "low stock", use stock < 20
- If asking for "never sold", use LEFT JOIN with NULL check
- If asking for "customers with no orders", use LEFT JOIN + IS NULL

=====================
EXAMPLES:
=====================

Q: Top 5 selling products  
A:
SELECT p.name, SUM(oi.quantity) AS total_sold
FROM order_items oi
JOIN products p ON oi.product_id = p.id
GROUP BY p.name
ORDER BY total_sold DESC
LIMIT 5

Q: Products with low stock  
A:
SELECT name, stock
FROM products
WHERE stock < 20

Q: Customers who never placed orders  
A:
SELECT c.name
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
WHERE o.id IS NULL

=====================
USER QUESTION:
=====================
{user_query}
"""
    return call_llm(prompt)


def fix_sql(user_query: str, sql: str):
    prompt = prompt = f"""
You are an expert MySQL SQL debugger and optimizer.

Your task is to FIX the given SQL query so that it becomes:
- syntactically correct
- logically correct
- executable in MySQL

=====================
DATABASE SCHEMA:
=====================
products(id, name, category, price, stock)
orders(id, customer_id, date, total_amount)
order_items(id, order_id, product_id, quantity)
customers(id, name, city)

=====================
STRICT RULES:
=====================
1. ONLY return a valid SELECT SQL query
2. DO NOT return any explanation
3. DO NOT include markdown (NO ```sql or ```)
4. DO NOT include comments
5. Output must be plain SQL only
6. DO NOT include semicolon (;) at the end

=====================
WHAT TO FIX:
=====================
- Remove markdown formatting like ```sql
- Fix syntax errors (missing commas, wrong keywords, etc.)
- Fix incorrect table or column names
- Fix wrong joins based on schema
- Ensure correct GROUP BY when using aggregation
- Ensure correct ORDER BY for sorting queries
- Add LIMIT if missing (default LIMIT 100)
- Remove invalid or unsupported SQL parts
- Ensure all columns are properly referenced with table aliases

=====================
JOIN RULES:
=====================
- orders.customer_id = customers.id
- order_items.order_id = orders.id
- order_items.product_id = products.id

=====================
EDGE CASE HANDLING:
=====================
- If aggregation is used → ensure GROUP BY
- If "top" or "highest" → use ORDER BY DESC
- If "low stock" → use stock < 20
- If query returns nothing → try logical correction
- If ambiguous → choose most logical business interpretation

=====================
USER QUESTION:
=====================
{user_query}

=====================
BROKEN SQL:
=====================
{sql}

=====================
OUTPUT:
=====================
Return ONLY the corrected SQL query.
"""
    return call_llm(prompt)