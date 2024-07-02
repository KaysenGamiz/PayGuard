import streamlit as st
from auth import authenticate_user, create_user, create_session, validate_session
from streamlit_extras.switch_page_button import switch_page
from time import sleep

st.set_page_config(layout="wide")

def main():
    st.title('Debt Tracker App')

    if 'session_token' not in st.session_state:
        st.session_state['session_token'] = None

    if st.session_state['session_token'] is None:
        username = st.text_input('Username')
        password = st.text_input('Password', type='password')
        if st.button('Login'):
            user = authenticate_user(username, password)
            if user:
                session_token = create_session(user[0])
                st.session_state['session_token'] = session_token
                st.session_state['user_id'] = user[0]
                st.success('Logged in successfully!')

                time = 1
                sleep(time)

                switch_page("user")
            else:
                st.error('Invalid username or password')

        st.markdown("---")
        st.markdown("### Create a new account")
        new_username = st.text_input('New Username')
        new_password = st.text_input('New Password', type='password')
        email = st.text_input('Email')
        if st.button('Create Account'):
            if new_username and new_password and email:
                user_id = create_user(new_username, new_password, email)
                if user_id:
                    st.success(f'Account created successfully for {new_username}!')
                else:
                    st.error('Failed to create account. Please try again.')
            else:
                st.error('Please fill all fields to create an account.')

    else:
        session = validate_session(st.session_state['session_token'])
        if session:
            st.success('Welcome back!')
            st.write("Redirecting to the dashboard...")
            st.session_state['page'] = 'dashboard'
            st.rerun()
        else:
            st.session_state['session_token'] = None
            st.error('Session expired. Please log in again.')

if __name__ == '__main__':
    main()
