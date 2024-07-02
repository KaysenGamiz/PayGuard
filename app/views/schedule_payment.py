import streamlit as st
import datetime
from utils import add_debt, get_user, get_debt_types

def schedule_payment_page():
    st.subheader("📆 Schedule Payment")

    user_id = get_user()

    debt_types = get_debt_types()
    debt_type_options = [debt_type['debt_type'] for debt_type in debt_types]
    debt_type_dict = {debt_type['debt_type']: debt_type['id'] for debt_type in debt_types}

    with st.form("debts"):
        st.write(f'User ID: {user_id}')

        amount = st.number_input('Amount', min_value=0.01, format="%.2f")
        due_date = st.date_input('Due Date', min_value=datetime.date.today())
        selected_type = st.selectbox('Debt Type', debt_type_options)
        description = st.text_area('Description')

        if st.form_submit_button('Schedule Payment'):
            type_id = debt_type_dict[selected_type]
            add_debt(user_id, amount, due_date, type_id, description)
            st.success('Payment scheduled successfully!')