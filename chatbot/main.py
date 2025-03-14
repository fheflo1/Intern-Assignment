from database.db import get_sql_database
from chatbot.agent import SQLAgent

def main():
    db = get_sql_database()
    agent = SQLAgent(db)
    print("Ask me a question or type 'exit' or 'quit' to stop.")
    while True:
        user_query = input("Ask me a question: ")
        if user_query.lower() in ['exit', 'quit']:
            break
        sql_query, result = agent.ask(user_query)
        print(f"SQL query: {sql_query}")
        print(f"Result: {result}")

if __name__ == '__main__':
    main()