import streamlit as st
import asyncio
from src.services.job_listener import JobListener
from src.services.auth_listener import AuthListener
from src.utils.custom_logger import CustomLogger
import pandas as pd

logger = CustomLogger("RecruiterPage")

def render_recruiter_page(user_data: dict):
    """Render the recruiter dashboard page"""
    try:
        # Initialize job listener
        job_listener = JobListener()
        if "token" in st.session_state:
            job_listener.update_token(st.session_state["token"])

        # Sidebar
        with st.sidebar:
            st.title("Recruiter Dashboard")
            st.title("Navigation")
            # Navigation: Remove Dashboard, set Profile as default
            selected_page = st.radio(
                "Go to",
                [
                    "Profile",
                    "Create Job",
                    "Search Jobs",
                    "Search Candidates",
                    "Rank Candidates"
                ],
                index=0,  # Profile is default
                label_visibility="collapsed"
            )
            st.divider()
            # Logout button
            if st.button("Sign Out", use_container_width=True, type="primary"):
                st.session_state.clear()
                st.rerun()

        # Main content area
        if selected_page == "Profile":
            render_profile_section(user_data)
        elif selected_page == "Create Job":
            render_create_job_section(job_listener)
        elif selected_page == "Search Jobs":
            render_manage_jobs_section(job_listener)
        elif selected_page == "Search Candidates":
            render_candidates_section(job_listener)
        elif selected_page == "Rank Candidates":
            render_rank_candidates_section(job_listener)

    except Exception as e:
        logger.error(f"Error in recruiter page: {str(e)}")
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

def render_create_job_section(job_listener: JobListener):
    """Render job creation section"""
    st.title("Create New Job")

    title = st.text_input("Job Title")
    company = st.text_input("Company")
    location = st.text_input("Location")
    required_experience = st.number_input("Required Experience (years)", min_value=0)
    job_description = st.text_area("Job Description")

    if st.button("Create Job", use_container_width=True, type="primary"):
        if title and company and location and job_description:
            job_data = {
                "title": title,
                "company": company,
                "location": location, 
                "required_experience": required_experience,
                "job_description": job_description
            }
            with st.spinner("Creating job posting..."):
                result = asyncio.run(job_listener.create_job(job_data))
                if "error" not in result:
                    st.success("Job posted successfully!")
                else:
                    st.error(f"Failed to create job: {result['error']}")
        else:
            st.warning("Please fill in all required fields")

def render_manage_jobs_section(job_listener: JobListener):
    """Render job management section"""
    st.title("Job Management")
    
    with st.container():
        st.subheader("Search Job")
        search_col1, search_col2 = st.columns([4, 1])
        with search_col1:
            job_id = st.text_input("Enter Job ID", placeholder="Enter the job ID to search", label_visibility="collapsed")
        with search_col2:
            search_clicked = st.button("Search", type="primary", use_container_width=True)

    if search_clicked and job_id:
        with st.spinner("Fetching job details..."):
            result = asyncio.run(job_listener.get_job(job_id))
            if "error" not in result:
                st.success("Job found")
                
                with st.expander("Job Details", expanded=True):
                    # Display job details in a more structured way
                    st.write("**Job Information**")
                    if isinstance(result, dict):
                        # Basic Information
                        st.subheader("Basic Information")
                        basic_fields = ["title", "company", "location", "required_experience"]
                        for field in basic_fields:
                            if field in result:
                                st.write(f"**{field.title()}:** {result[field]}")
                        
                        # Job Description
                        if "job_description" in result:
                            st.subheader("Job Description")
                            st.write(result["job_description"])
                        
                        # Parsed JD Categories
                        if "parsed_jd" in result:
                            st.subheader("Parsed Job Description")
                            parsed_jd = result["parsed_jd"]
                            
                            if isinstance(parsed_jd, dict):
                                # Display other categories
                                for category, items in parsed_jd.items():
                                    if category not in ["skills"]:
                                        st.markdown(f"**{category.title()}**")
                                        if isinstance(items, list):
                                            for item in items:
                                                st.write(f"• {item}")
                                        else:
                                            st.write(items)

                                # Display Technical Skills
                                if "skills" in parsed_jd:
                                    skills = parsed_jd["skills"]
                                    if "technical" in skills:
                                        st.markdown("**Technical Skills**")
                                        technical_skills = skills["technical"]
                                        if isinstance(technical_skills, list):
                                            for skill in technical_skills:
                                                st.markdown(f"• `{skill}`")
                                
                                    # Display Soft Skills
                                    if "soft" in skills:
                                        st.markdown("**Soft Skills**")
                                        soft_skills = skills["soft"]
                                        if isinstance(soft_skills, list):
                                            for skill in soft_skills:
                                                st.markdown(f"• `{skill}`")
                                
                    else:
                        st.json(result)
            else:
                st.warning("Job not created yet")
                logger.error(f"Failed to retrieve job details: {result['error']}")
    elif search_clicked:
        st.warning("Please enter a Job ID")

def render_candidates_section(job_listener: JobListener):
    """Render candidate search section"""
    st.title("Search Candidates")
    
    st.subheader("Search Filters")
    
    skills = st.text_input("Skills (comma-separated)")
    col1, col2 = st.columns(2)
    with col1:
        experience = st.number_input("Minimum Experience (years)", min_value=0)
    with col2:
        location = st.text_input("Location")
    
    if st.button("Search Candidates", use_container_width=True, type="primary"):
        search_params = {
            "skills": skills,
            "experience": experience,
            "location": location
        }
        
        with st.spinner("Searching candidates..."):
            result = asyncio.run(job_listener.search_candidates(search_params))
            if isinstance(result, list):
                st.success(f"Found {len(result)} candidates!")
                for candidate in result:
                    with st.expander(f"Candidate ID: {candidate.get('id', 'N/A')}", expanded=False):
                        st.write("**Candidate Information**")
                        # Personal Information
                        if "parsed_resume" in candidate:
                            if candidate['parsed_resume']['personal_info']:
                                st.subheader("Personal Information")
                                for key, value in candidate['parsed_resume']['personal_info'].items():
                                    if value:  # Only show non-empty values
                                        st.write(f"**{key.title()}:** {value}")

                            # Experience
                            if candidate['parsed_resume']['experience']:
                                st.subheader("Experience")
                                for exp in candidate['parsed_resume']['experience']:
                                    st.write(f"**{exp.get('title')} at {exp.get('company')}**")
                                    st.write(f"*{exp.get('period')}*")
                                    for resp in exp.get('responsibilities', []):
                                        st.write(f"• {resp}")

                            # Education
                            if candidate['parsed_resume']['education']:
                                st.subheader("Education")
                                for edu in candidate['parsed_resume']['education']:
                                    st.write(f"**{edu.get('degree')}**")
                                    st.write(f"*{edu.get('institution')}* ({edu.get('period')})")

                            # Skills
                            if candidate['parsed_resume']['skills']:
                                if candidate['parsed_resume']['skills']['technical']:
                                    st.subheader("Technical Skills")
                                    for skill in candidate['parsed_resume']['skills']['technical']:
                                        st.markdown(f"• `{skill}`")
                                if candidate['parsed_resume']['skills']['soft']:
                                    st.subheader("Soft Skills")
                                    for skill in candidate['parsed_resume']['skills']['soft']:
                                        st.markdown(f"• `{skill}`")

                            # Certifications
                            if candidate['parsed_resume']['certifications']:
                                st.subheader("Certifications")
                                for cert in candidate['parsed_resume']['certifications']:
                                    st.write(f"• {cert}")

                            # Languages
                            if candidate['parsed_resume']['languages']:
                                st.subheader("Languages")
                                for lang in candidate['parsed_resume']['languages']:
                                    st.write(f"• {lang}")
            elif isinstance(result, dict) and "error" in result:
                logger.error(f"Search failed: {result['error']}")
                st.warning("At least one of the fields is required")
            else:
                st.error("Unexpected response format from search")

def render_rank_candidates_section(job_listener: JobListener):
    """Render the candidate ranking section by Job ID"""
    st.title("Rank Candidates by Job")
    job_id = st.text_input("Enter Job ID to rank candidates")
    col1, col2 = st.columns(2)
    with col1:
        min_score = st.number_input("Minimum Score", min_value=0.0, max_value=100.0, value=0.0, step=0.1)
    with col2:
        limit = st.number_input("Limit", min_value=1, max_value=100, value=10, step=1)
    if st.button("Rank Candidates", use_container_width=True, type="primary"):
        if job_id:
            with st.spinner("Ranking candidates..."):
                # Pass min_score and limit as params
                params = {"job_id": job_id, "min_score": min_score, "limit": int(limit)}
                result = asyncio.run(job_listener.rank_candidates_with_params(params))
                if "error" not in result:
                    # Robust handling for both dict and list
                    if isinstance(result, list):
                        candidates = result
                    elif isinstance(result, dict):
                        candidates = result.get("candidates", [])
                    else:
                        candidates = []
                    if candidates:
                        st.success(f"Found {len(candidates)} ranked candidates!")
                        for candidate in candidates:
                            with st.expander(f"Candidate ID: {candidate.get('id', 'N/A')}", expanded=False):
                                st.write("**Candidate Information**")
                                # Personal Information
                                if "parsed_resume" in candidate:
                                    if candidate['parsed_resume']['personal_info']:
                                        st.subheader("Personal Information")
                                        for key, value in candidate['parsed_resume']['personal_info'].items():
                                            if value:  # Only show non-empty values
                                                st.write(f"**{key.title()}:** {value}")

                                    # Experience
                                    if candidate['parsed_resume']['experience']:
                                        st.subheader("Experience")
                                        for exp in candidate['parsed_resume']['experience']:
                                            st.write(f"**{exp.get('title')} at {exp.get('company')}**")
                                            st.write(f"*{exp.get('period')}*")
                                            for resp in exp.get('responsibilities', []):
                                                st.write(f"• {resp}")

                                    # Education
                                    if candidate['parsed_resume']['education']:
                                        st.subheader("Education")
                                        for edu in candidate['parsed_resume']['education']:
                                            st.write(f"**{edu.get('degree')}**")
                                            st.write(f"*{edu.get('institution')}* ({edu.get('period')})")

                                    # Skills
                                    if candidate['parsed_resume']['skills']:
                                        if candidate['parsed_resume']['skills']['technical']:
                                            st.subheader("Technical Skills")
                                            for skill in candidate['parsed_resume']['skills']['technical']:
                                                st.markdown(f"• `{skill}`")
                                        if candidate['parsed_resume']['skills']['soft']:
                                            st.subheader("Soft Skills")
                                            for skill in candidate['parsed_resume']['skills']['soft']:
                                                st.markdown(f"• `{skill}`")

                                    # Certifications
                                    if candidate['parsed_resume']['certifications']:
                                        st.subheader("Certifications")
                                        for cert in candidate['parsed_resume']['certifications']:
                                            st.write(f"• {cert}")

                                    # Languages
                                    if candidate['parsed_resume']['languages']:
                                        st.subheader("Languages")
                                        for lang in candidate['parsed_resume']['languages']:
                                            st.write(f"• {lang}")

                                st.subheader("Ranking Information")
                                if 'match_scores' in candidate:
                                    for score_type in candidate['match_scores']:
                                        st.write(f"**{score_type}:** {candidate['match_scores'][score_type]}")
                    else:
                        st.info("No candidates ranked for this job.")
                else:
                    st.error(f"Failed to rank candidates: {result['error']}")
        else:
            st.warning("Please enter a Job ID")

if __name__ == "__main__":
    render_recruiter_page({})