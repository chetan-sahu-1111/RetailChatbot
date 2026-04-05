from sqlalchemy import create_engine, text
from app.core.config import DATABASE_URL

engine = create_engine(DATABASE_URL)

def run_sql(query: str):
    with engine.connect() as conn:
        result = conn.execute(text(query))
        return [dict(row._mapping) for row in result]