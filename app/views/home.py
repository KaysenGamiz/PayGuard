import streamlit as st
import datetime
from utils import get_unpaid_debts, get_user, get_openai_response, update_debt, convert_df_to_string
from time import sleep

column_config = {
    "id": st.column_config.Column(label="ID"),
    "amount": st.column_config.NumberColumn(label="Amount", format="$%.2f"),
    "due_date": st.column_config.DateColumn(label="Due Date"),
    "description": st.column_config.Column(label="Description"), 
    "ispaid": st.column_config.CheckboxColumn(label="Is Paid?"),
    "created_at": st.column_config.DatetimeColumn(label="Created At"),
    "debt_type": st.column_config.Column(label="Payment Type")
}

def home_page():

    st.subheader("🏠 Home")

    user_id = get_user()

    df = get_unpaid_debts(user_id)
    debts_info = convert_df_to_string(df)

    if df.empty:
        st.success("You have no debts!")
    else:
        new_df = st.data_editor(df, hide_index=True, disabled=["id", "created_at", 'debt_type'], width=5000, column_config=column_config)

        if st.button("Submit Changes"):
            for index, row in new_df.iterrows():
                debt_id = row["id"]
                amount = row["amount"]
                due_date = row["due_date"]
                description = row["description"]
                is_paid = row["ispaid"]
                update_debt(debt_id, amount, due_date, description, is_paid)
            st.success("Changes submitted successfully!")

            time = .5
            sleep(time)
            st.rerun()


    st.subheader("ChatGPT Chatbox")

    # Inicializa la lista de mensajes en la sesión
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Muestra la conversación en un contenedor
    with st.container(border=True, height=345):
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.chat_message("user").write(message['content'])
            else:
                st.chat_message("assistant").write(message['content'])

    # Entrada de chat usando chat_input
    if prompt := st.chat_input("Escribe tu mensaje..."):
        # Añade el mensaje del usuario a la lista de mensajes
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Obtiene la respuesta de OpenAI
        openai_response = get_openai_response(prompt, debts_info)
        
        # Añade la respuesta de OpenAI a la lista de mensajes
        st.session_state.messages.append({"role": "assistant", "content": openai_response})

        # Refresca la página para mostrar la conversación actualizada
        st.experimental_rerun()

    # Borrar el historial de la conversación
    if st.button("Borrar conversación"):
        st.session_state.messages = []
        st.experimental_rerun()