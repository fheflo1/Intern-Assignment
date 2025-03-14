import streamlit as st
from database.db import get_sql_database
from chatbot.agent import SQLAgent

def main():
    st.title("👨‍🦯‍➡️GISpion👀")

    db = get_sql_database()
    agent = SQLAgent(db)

    user_query = st.text_input("Ask me a question:")
    if st.button("Submit"):
        if user_query.strip():
            sql_query, result = agent.ask(user_query)
            st.write("**SQL query:**", sql_query)
            st.write("**Result:**", result)
        else:
            st.write("Please enter a question.")

if __name__ == '__main__':
    main()