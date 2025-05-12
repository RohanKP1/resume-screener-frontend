import os
import streamlit as st
import asyncio
from src.services.auth_listener import AuthListener
from src.services.candidate_listener import CandidateListener
from src.utils.custom_logger import CustomLogger

logger = CustomLogger("CandidatePage")

def render_candidate_page(user_data: dict):
    """Render the candidate dashboard page"""
    try:
        candidate_listener = CandidateListener()
        if "token" in st.session_state:
            candidate_listener.update_token(st.session_state["token"])

        # Sidebar
        with st.sidebar:
            # User profile in sidebar
            st.title("Candidate Dashboard")
            st.title("Navigation")
            
            # Navigation
            selected_page = st.radio(
                "Navigation",
                ["Profile", "Resume Management"],
                label_visibility="collapsed"
            )
            
            st.divider()
            
            # Logout button
            if st.button("Sign Out", type="primary", use_container_width=True):
                st.session_state.clear()
                st.rerun()

        # Main content area
        if selected_page == "Profile":
            render_profile_section(user_data)
        elif selected_page == "Resume Management":
            render_resume_section(candidate_listener, user_data)

    except Exception as e:
        logger.error(f"Error in candidate page: {str(e)}")
        st.error("An unexpected error occurred. Please try again later.")

def render_profile_section(user_data: dict):
    """Render recruiter profile section"""
    st.title("My Profile")
    
    # Profile information using columns
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Username:**")
            st.write("**Email:**")
            st.write("**Role:**")
        with col2:
            st.write(user_data.get('username', 'N/A'))
            st.write(user_data.get('email', 'N/A'))
            st.write(user_data.get('user_type', 'RECRUITER'))
    
    st.divider()
    
    # Profile update form
    st.subheader("Update Profile")
    with st.form("profile_update_form"):
        new_username = st.text_input("New Username")
        new_email = st.text_input("New Email")
        submitted = st.form_submit_button("Update Profile", use_container_width=True)

        if submitted:
            update_data = {}
            if new_username:
                update_data["username"] = new_username
            if new_email:
                update_data["email"] = new_email

            if update_data:
                auth_listener = AuthListener()
                if "token" in st.session_state:
                    auth_listener.update_token(st.session_state["token"])
                result = asyncio.run(auth_listener.update_profile(update_data))
                if "error" not in result:
                    # Update session state and show success
                    st.session_state["user_data"].update(update_data)
                    st.success("Profile updated successfully!")
                else:
                    st.error(f"Profile update failed: {result['error']}")
            else:
                st.info("Please enter a new username or email to update.")

def render_resume_section(candidate_listener: CandidateListener, user_data: dict):
    """Render resume management section"""
    st.title("Resume Management")
    
    # Upload section using container
    with st.container():
        st.subheader("Upload Resume")
        uploaded_file = st.file_uploader(
            "Choose PDF or DOCX file",
            type=['pdf', 'docx']
        )
    
        if uploaded_file:
            temp_path = f"temp_{uploaded_file.name}"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("Upload Resume", type="primary", use_container_width=True):
                    with st.spinner("Uploading..."):
                        result = asyncio.run(
                            candidate_listener.upload_resume(temp_path, user_data.get('id'))
                        )
                        
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
                        
                    if "error" not in result:
                        st.success("Resume uploaded successfully!")
                    else:
                        st.error(result["error"])
    
    st.divider()
    
    # Current resume section
    st.subheader("Current Resume")
    if st.button("View Resume", use_container_width=True):
        with st.spinner("Loading..."):
            result = asyncio.run(candidate_listener.get_resume(user_data.get('id')))
            
        if "error" not in result:
            with st.expander(f"Candidate ID: {user_data.get('id', 'N/A')}", expanded=True):
                st.write("**Candidate Information**")
                # Personal Information
                if "parsed_resume" in result:
                    if result['parsed_resume']['personal_info']:
                        st.subheader("Personal Information")
                        for key, value in result['parsed_resume']['personal_info'].items():
                            if value:  # Only show non-empty values
                                st.write(f"**{key.title()}:** {value}")
                    # Experience
                    if result['parsed_resume']['experience']:
                        st.subheader("Experience")
                        for exp in result['parsed_resume']['experience']:
                            st.write(f"**{exp.get('title')} at {exp.get('company')}**")
                            st.write(f"*{exp.get('period')}*")
                            for resp in exp.get('responsibilities', []):
                                st.write(f"• {resp}")
                        st.write("**Total Experience:**", result['total_experience'], "years")        

                    # Education
                    if result['parsed_resume']['education']:
                        st.subheader("Education")
                        for edu in result['parsed_resume']['education']:
                            st.write(f"**{edu.get('degree')}**")
                            st.write(f"*{edu.get('institution')}* ({edu.get('period')})")

                    # Skills
                    if result['parsed_resume']['skills']:
                        if result['parsed_resume']['skills']['technical']:
                            st.subheader("Technical Skills")
                            for skill in result['parsed_resume']['skills']['technical']:
                                st.markdown(f"• `{skill}`")
                        if result['parsed_resume']['skills']['soft']:
                            st.subheader("Soft Skills")
                            for skill in result['parsed_resume']['skills']['soft']:
                                st.markdown(f"• `{skill}`")

                    # Certifications
                    if result['parsed_resume']['certifications']:
                        st.subheader("Certifications")
                        for cert in result['parsed_resume']['certifications']:
                            st.write(f"• {cert}")

                    # Languages
                    if result['parsed_resume']['languages']:
                        st.subheader("Languages")
                        for lang in result['parsed_resume']['languages']:
                            st.write(f"• {lang}") 

                st.subheader("Raw Text")
                if "raw_text" in result:
                    st.text_area("Extracted Text", result['raw_text'], height=300)                                           

        else:
            st.error("Failed to load resume")

