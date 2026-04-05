from fastapi import APIRouter
from app.models.request_models import QueryRequest
from app.services.sql_service import generate_sql, fix_sql
from app.services.validation import is_safe_query, add_limit, uses_valid_tables, validate_result
from app.db.database import run_sql
from app.core.logger import get_logger
from app.utils.helper import clean_sql

router = APIRouter()
logger = get_logger(__name__)

@router.post("/chat")

def chat(request: QueryRequest):
    user_query = request.query
    logger.info(f"User Query: {user_query}")

    # Step 1: Generate SQL
    sql = generate_sql(user_query)
    sql = clean_sql(sql) 
    logger.info(f"Generated SQL: {sql}")

    # Step 2: Safety check
    if not is_safe_query(sql):
        return {"error": "Unsafe query detected"}

    # Step 3: Table validation
    if not uses_valid_tables(sql):
        sql = fix_sql(user_query, sql)
        sql = clean_sql(sql) 

    # Step 4: Add LIMIT
    sql = add_limit(sql)

    try:
        # Step 5: Execute
        result = run_sql(sql)
        sql = clean_sql(sql) 

        # Step 6: Validate result
        if not validate_result(result):
            sql = fix_sql(user_query, sql)
            sql = clean_sql(sql) 
            result = run_sql(sql)
            sql = clean_sql(sql) 

        return {
            "query": user_query,
            "final_sql": sql,
            "result": result
        }

    except Exception as e:
        logger.warning("Empty result, retrying...")
        # Step 7: Auto-retry on error
        try:
            sql = fix_sql(user_query, sql)
            sql = clean_sql(sql) 
            result = run_sql(sql)
            sql = clean_sql(sql) 

            return {
                "query": user_query,
                "fixed_sql": sql,
                "result": result
            }
        except:
            logger.error(f"Error: {str(e)}")
            return {"error": str(e)}