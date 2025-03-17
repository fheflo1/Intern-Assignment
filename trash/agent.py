import re
from langchain_community.utilities import SQLDatabase
from trash.llm import load_few_shot_prompts, create_llm


class SQLAgent:
    def __init__(self, db: SQLDatabase):
        self.db = db
        self.llm = create_llm()
        self.few_shot, self.fix_prompt = load_few_shot_prompts()

    def generate_sql(self, user_query: str) -> str:
        prompt = self.few_shot.replace("{query}", user_query)
        sql_query = self.llm._call(prompt)
        return sql_query.strip()
    
    def fix_sql(self, sql_query: str, error_message: str) -> str:
        fix_prompt = self.fix_prompt.format(
            sql_query=sql_query,
            error_message=error_message
        )
        new_sql = self.llm._call(fix_prompt)
        return new_sql.strip()
    
    def validate_sql(self, sql_query: str) -> bool:
        forbidden_keywords = ['delete', 'update', 'insert', 'alter', 'drop', 'truncate']
        pattern = r"\b(" + "|".join(forbidden_keywords) + r")\b"
        if re.search(pattern, sql_query.lower()):
            return False
        return True
    
    def execute_sql(self, sql_query: str):
        return self.db.run(sql_query)
    
    def ask(self, user_query: str):
        sql_query = self.generate_sql(user_query)
        if not self.validate_sql(sql_query):
            return None, "Invalid query. Please try again."
        try:
            result = self.execute_sql(sql_query)
            return sql_query, result
        except Exception as e:
            fix_attempt = self.fix_sql(sql_query, str(e))
            if not self.validate_sql(fix_attempt):
                return None, f"Error when attempting to fix query: {e}"
            
            try:
                result2 = self.execute_sql(fix_attempt)
                return (fix_attempt, result2)
            except Exception as e2:
                return (fix_attempt, f"Error when executing fixed query: {e2}")