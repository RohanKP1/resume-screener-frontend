import streamlit as st
import asyncio
from src.services.auth_listener import AuthListener
from src.utils.custom_logger import CustomLogger

logger = CustomLogger("AuthPage")

def render_login_page():
    st.title("Welcome Back!")
    
    auth_listener = AuthListener()
    
    with st.form("login_form", clear_on_submit=True):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        col1, col2 = st.columns([1, 1])
        
        with col1:
            submit = st.form_submit_button("Login", use_container_width=True, type="primary")
        with col2:
            if st.form_submit_button("Don't have an account? Sign up", use_container_width=True):
                st.session_state.show_register = True
                st.rerun()
        
        if submit:
            result = asyncio.run(auth_listener.login(username, password))
            logger.debug(f"Login result: {result}")
            
            if "error" not in result:
                st.session_state.update({
                    "token": result["access_token"],
                    "user_type": result.get("user_type"),
                    "user_data": {
                        "id": result.get("user_id"),
                        "username": username,
                        "email": result.get("email"),
                        "user_type": result.get("user_type")
                    },
                    "is_authenticated": True
                })
                logger.info(f"User logged in successfully: {username}")
                st.success("Successfully logged in!")
                st.rerun()
            else:
                logger.error(f"Login failed: {result['error']}")
                st.error(result["error"])

def render_register_page():
    st.title("Create Account")
    
    auth_listener = AuthListener()
    
    with st.form("register_form", clear_on_submit=True):
        new_username = st.text_input("Username")
        email = st.text_input("Email")
        new_password = st.text_input("Password", type="password")
        user_type = st.selectbox("User Type", ["candidate", "recruiter"])
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            submit = st.form_submit_button("Register", use_container_width=True, type="primary")
        with col2:
            if st.form_submit_button("Already have an account? Login", use_container_width=True):
                st.session_state.show_register = False
                st.rerun()
        
        if submit:
            result = asyncio.run(auth_listener.register(
                new_username, 
                email, 
                new_password, 
                user_type
            ))
            
            if "error" not in result:
                logger.info(f"User registered successfully: {email}")
                st.success("Successfully registered! Please login.")
                st.session_state.show_register = False
                st.rerun()
            else:
                logger.error(f"Registration failed: {result['error']}")
                st.error(result["error"])

def render_profile_update():
    st.title("Update Profile")
    auth_listener = AuthListener()
    
    with st.form("update_profile_form"):
        update_username = st.text_input("New Username (optional)")
        update_email = st.text_input("New Email (optional)")
        
        if st.form_submit_button("Update Profile", use_container_width=True):
            update_data = {}
            if update_username:
                update_data["username"] = update_username
            if update_email:
                update_data["email"] = update_email
                
            result = asyncio.run(auth_listener.update_profile(update_data))
            
            if "error" not in result:
                st.session_state["user_data"].update(update_data)
                logger.info("Profile updated successfully")
                st.success("Profile updated successfully!")
            else:
                logger.error(f"Profile update failed: {result['error']}")
                st.error(result["error"])

def render_auth_page():
    if "show_register" not in st.session_state:
        st.session_state.show_register = False
    
    if st.session_state.show_register:
        render_register_page()
    else:
        render_login_page()
    
    if "is_authenticated" in st.session_state and st.session_state["is_authenticated"]:
        render_profile_update()

if __name__ == "__main__":
    render_auth_page()