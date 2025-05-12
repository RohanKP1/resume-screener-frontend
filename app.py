import streamlit as st
from src.pages.auth_page import render_auth_page
from src.pages.candidate_page import render_candidate_page
from src.pages.recruiter_page import render_recruiter_page
from src.utils.custom_logger import CustomLogger

# Initialize logger
logger = CustomLogger("MainApp")

def main():
    """Main application entry point"""
    try:
        # Set page config
        st.set_page_config(
            page_title="Resume Ranker",
            page_icon="📄"
        )

        # Check authentication state
        if "token" not in st.session_state:
            logger.info("User not authenticated - rendering auth page")
            render_auth_page()
        else:
            # Get user type from session state
            user_type = st.session_state.get("user_type", "")
            user_data = st.session_state.get("user_data", {})
            logger.info(f"user_type: {user_type}")
            logger.info(f"user_data: {user_data}")
            
            if user_type == "candidate":
                logger.info("Rendering candidate dashboard")
                render_candidate_page(user_data)
            elif user_type == "recruiter":
                logger.info("Rendering recruiter dashboard")
                render_recruiter_page(user_data)
            else:
                logger.info("User type not recognized - rendering auth page")
                render_auth_page()

    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        st.error("An unexpected error occurred. Please try again later.")

if __name__ == "__main__":
    main()