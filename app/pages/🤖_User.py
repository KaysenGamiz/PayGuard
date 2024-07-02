import streamlit as st
from views.schedule_payment import schedule_payment_page
from views.home import home_page
from views.settings import settings_page

def user_dashboard():
    st.title('User Dashboard')

    user_id = st.session_state.get('user_id', None)
    if user_id:
        st.write(f'Welcome, User {user_id}!')
        st.sidebar.title("Menu")
        
        menu_options = ["🏠 Home", "📆 Schedule Payment", "⚙️ Settings"]
        page = st.sidebar.radio("Navigate", menu_options)

        # Insert CSS for the logout button at the bottom
        st.markdown(
            """
            <style>
            .css-1lcbmhc {
                display: flex;
                flex-direction: column;
                height: 100vh;
                justify-content: space-between;
            }
            </style>
            """, unsafe_allow_html=True
        )

        if page == "🏠 Home":
            home_page()
        elif page == "📆 Schedule Payment":
            schedule_payment_page()
        elif page == "⚙️ Settings":
            settings_page()

        # Create a placeholder at the bottom of the sidebar for the logout button
        logout_placeholder = st.sidebar.empty()
        with logout_placeholder:
            if st.sidebar.button('Logout', key='logout_bottom'):
                st.session_state['session_token'] = None
                st.session_state['user_id'] = None
                st.session_state['page'] = 'login'
                st.success('Logged out successfully')
                st.experimental_rerun()

    else:
        st.error("Please log in first.")
        st.stop()

if __name__ == "__main__":
    user_dashboard()
