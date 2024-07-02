from db import get_db_connection
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI
from psycopg2.extras import RealDictCursor
import os

load_dotenv()

client = OpenAI(
  api_key=os.environ.get("OPENAI_API_KEY"),
)

def get_debt_types():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute("SELECT id, debt_type FROM debt_types")
        debt_types = cur.fetchall()
        return debt_types
    finally:
        cur.close()
        conn.close()


def add_debt(user_id, amount, due_date, type_id, description, paid=False):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO debts (user_id, amount, due_date, type_id, description, isPaid)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (user_id, amount, due_date, type_id, description, paid)
    )
    conn.commit()
    cur.close()
    conn.close()


def update_debt(debt_id, amount, due_date, description, is_paid):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE debts
        SET amount = %s, due_date = %s, description = %s, isPaid = %s
        WHERE id = %s
    """, (amount, due_date, description, is_paid, debt_id))
    conn.commit()
    cur.close()
    conn.close()


def get_unpaid_debts(user_id):
    conn = get_db_connection()
    query = """
        SELECT d.id, d.amount, d.due_date, d.description, dt.debt_type, d.ispaid, d.created_at
        FROM debts as d
        JOIN debt_types dt on d.type_id = dt.id
        WHERE user_id = %s AND ispaid = FALSE
    """
    df = pd.read_sql_query(query, conn, params=(user_id,))
    conn.close()
    return df


def get_user():
    user_id = st.session_state.get('user_id', None)
    if not user_id:
        st.error("You need to be logged in to schedule a payment.")
        st.stop()
    
    return user_id
 

def get_openai_response(prompt, debts_info):
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Eres un analista financiero experto"
                    )
                },
                {
                    "role": "user",
                    "content": f"Estos son los detalles de las deudas:\n{debts_info}\n\n{prompt}"
                }
            ]
        )
        
        completion = response.choices[0].message.content

        return completion
    except Exception as e:
        return str(e)


def convert_df_to_string(df):
    return df.to_string(index=False)
