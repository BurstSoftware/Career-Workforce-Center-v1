import streamlit as st
import pandas as pd

# Set page configuration
st.set_page_config(page_title="Career Workforce Center", layout="wide")

# App title and description
st.title("Welcome to the Career Workforce Center")
st.markdown("""
This platform provides free services to support job seekers and employers. Explore job opportunities, access career counseling, learn about training programs, or find recruitment solutions.
""")

# Sample job data (replace with real data or API in production)
job_listings = pd.DataFrame({
    "Job Title": ["Software Engineer", "Registered Nurse", "Warehouse Associate", "Marketing Coordinator"],
    "Company": ["TechCorp", "HealthSys", "Logistics Inc.", "Creative Agency"],
    "Location": ["Austin, TX", "Houston, TX", "Dallas, TX", "San Antonio, TX"],
    "Salary": ["$90,000 - $120,000", "$70,000 - $85,000", "$35,000 - $45,000", "$50,000 - $65,000"],
    "Posted Date": ["2025-06-01", "2025-06-03", "2025-06-05", "2025-06-07"]
})

# Sample training programs
training_programs = pd.DataFrame({
    "Program": ["Web Development Bootcamp", "Nursing Assistant Certification", "Forklift Operator Training", "Digital Marketing Course"],
    "Provider": ["CodeAcademy", "HealthEd", "SafetyFirst", "MarketPro"],
    "Duration": ["12 weeks", "8 weeks", "1 week", "10 weeks"],
    "Cost": ["Free (funded)", "$500", "$200", "Free (funded)"]
})

# Sidebar for user type selection
st.sidebar.header("Who Are You?")
user_type = st.sidebar.radio("Select your role:", ("Job Seeker", "Employer"))

# Main content based on user type
if user_type == "Job Seeker":
    st.header("Services for Job Seekers")
    
    # Tabs for different services
    tab1, tab2, tab3, tab4 = st.tabs(["Job Search", "Career Counseling", "Resume Tips", "Training Programs"])
    
    with tab1:
        st.subheader("Find a Job")
        st.write("Search through available job listings in your area.")
        # Job search filter
        search_term = st.text_input("Enter job title or keyword:")
        location_filter = st.selectbox("Filter by location:", ["All"] + job_listings["Location"].unique().tolist())
        
        # Filter job listings
        filtered_jobs = job_listings
        if search_term:
            filtered_jobs = filtered_jobs[filtered_jobs["Job Title"].str.contains(search_term, case=False, na=False)]
        if location_filter != "All":
            filtered_jobs = filtered_jobs[filtered_jobs["Location"] == location_filter]
        
        st.dataframe(filtered_jobs, use_container_width=True)
        if st.button("Apply for Selected Job"):
            st.success("Application submitted! Check your email for next steps.")
    
    with tab2:
        st.subheader("Career Counseling")
        st.write("Get personalized career advice to plan your next steps.")
        career_goal = st.text_area("What are your career goals?")
        if st.button("Submit for Counseling"):
            st.info(f"Thank you! A career counselor will contact you to discuss: {career_goal}")
    
    with tab3:
        st.subheader("Resume and Interview Tips")
        st.markdown("""
        - **Resume Tips**: Use action verbs, quantify achievements, and tailor your resume to the job.
        - **Interview Tips**: Practice common questions, research the company, and dress professionally.
        """)
        st.download_button(
            label="Download Resume Template",
            data="Resume Template Content",  # Replace with actual file content
            file_name="resume_template.docx",
            mime="application/octet-stream"
        )
    
    with tab4:
        st.subheader("Explore Training Programs")
        st.write("Find training to gain skills for in-demand jobs.")
        st.dataframe(training_programs, use_container_width=True)
        selected_program = st.selectbox("Select a program to learn more:", training_programs["Program"])
        if st.button("Request Program Info"):
            st.success(f"Information about {selected_program} has been sent to your email.")

elif user_type == "Employer":
    st.header("Services for Employers")
    
    # Tabs for employer services
    tab1, tab2 = st.tabs(["Post a Job", "Recruitment Support"])
    
    with tab1:
        st.subheader("Post a Job Opening")
        job_title = st.text_input("Job Title")
        company = st.text_input("Company Name")
        location = st.text_input("Location")
        salary = st.text_input("Salary Range")
        job_description = st.text_area("Job Description")
        
        if st.button("Post Job"):
            st.success(f"Job '{job_title}' posted successfully! We'll notify you when candidates apply.")
    
    with tab2:
        st.subheader("Recruitment Support")
        st.write("Get help finding qualified candidates.")
        st.markdown("""
        - **Screening**: We review resumes to match your job requirements.
        - **Job Fairs**: Participate in our upcoming hiring events.
        - **Tax Credits**: Learn about incentives like the Work Opportunity Tax Credit.
        """)
        if st.button("Request Recruitment Assistance"):
            st.info("A recruitment specialist will contact you soon.")

# Footer
st.markdown("---")
st.markdown("""
**Career Workforce Center** | Free services for job seekers and employers.  
Visit us at [CareerOneStop.org](https://www.careeronestop.org) or contact your local workforce agency.
""")
