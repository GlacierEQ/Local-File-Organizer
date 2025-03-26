# Streamlit dashboard for document search.
import streamlit as st
import psycopg2

conn = psycopg2.connect("dbname=ai_docs user=postgres password=yourpassword")

st.title("📂 AI Document Search")

query = st.text_input("Enter Search Query:")
if query:
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT filename, content 
            FROM documents 
            WHERE search_vector @@ to_tsquery('english', %s)
            ORDER BY id DESC LIMIT 10;
            """, 
            (query,)
        )
        results = cur.fetchall()

    for filename, content in results:
        st.subheader(filename)
        st.write(content[:500] + "...")
