import streamlit as st
import pandas as pd
from fuzzywuzzy import fuzz  # For job matching
import re

# Set page configuration
st.set_page_config(page_title="Career Workforce Center with AI Agents", layout="wide")

# Sample job and training data (replace with real data or API in production)
job_listings = pd.DataFrame({
    "Job Title": ["Software Engineer", "Registered Nurse", "Warehouse Associate", "Marketing Coordinator"],
    "Company": ["TechCorp", "HealthSys", "Logistics Inc.", "Creative Agency"],
    "Location": ["Austin, TX", "Houston, TX", "Dallas, TX", "San Antonio, TX"],
    "Salary": ["$90,000 - $120,000", "$70,000 - $85,000", "$35,000 - $45,000", "$50,000 - $65,000"],
    "Skills": ["Python, Java", "Nursing, Patient Care", "Forklift, Inventory", "SEO, Social Media"],
    "Posted Date": ["2025-06-01", "2025-06-03", "2025-06-05", "2025-06-07"]
})

training_programs = pd.DataFrame({
    "Program": ["Web Development Bootcamp", "Nursing Assistant Certification", "Forklift Operator Training", "Digital Marketing Course"],
    "Provider": ["CodeAcademy", "HealthEd", "SafetyFirst", "MarketPro"],
    "Duration": ["12 weeks", "8 weeks", "1 week", "10 weeks"],
    "Cost": ["Free (funded)", "$500", "$200", "Free (funded)"]
})

# Agent Classes
class EmmaHarper:
    """Job Matching Agent"""
    def __init__(self, job_data):
        self.job_data = job_data
    
    def match_jobs(self, keywords, location=None, skills=None):
        """Match jobs based on keywords, location, and skills using fuzzy matching."""
        matches = self.job_data.copy()
        if keywords:
            matches['Score'] = matches['Job Title'].apply(lambda x: fuzz.partial_ratio(keywords.lower(), x.lower()))
            matches = matches[matches['Score'] > 70]  # Threshold for relevance
        if location and location != "All":
            matches = matches[matches['Location'] == location]
        if skills:
            matches = matches[matches['Skills'].str.contains(skills, case=False, na=False)]
        return matches.sort_values(by='Score', ascending=False) if 'Score' in matches.columns else matches

class MasonCole:
    """Career Counseling Agent"""
    def provide_advice(self, goals):
        """Provide career advice based on user goals."""
        if not goals:
            return "Please share your career goals, and I'll provide tailored advice!"
        if "career change" in goals.lower():
            return "Considering a career change? Explore in-demand fields like tech or healthcare. I recommend checking our training programs for new skills."
        elif "promotion" in goals.lower():
            return "Aiming for a promotion? Focus on leadership skills and certifications. Try our resume review service to strengthen your application."
        else:
            return "Your goals sound exciting! Let's start with a skills assessment and explore job opportunities that align with your interests."

class AvaQuinn:
    """Resume Review Agent"""
    def review_resume(self, resume_text):
        """Analyze resume text and provide improvement suggestions."""
        if not resume_text:
            return "Please provide your resume text for review."
        suggestions = []
        if len(resume_text.split()) < 50:
            suggestions.append("Your resume seems too short. Add more details about your experience and achievements.")
        if not re.search(r"\b\d+\b", resume_text):
            suggestions.append("Include quantifiable achievements (e.g., 'Increased sales by 20%').")
        if not re.search(r"python|java|sql", resume_text, re.IGNORECASE):
            suggestions.append("Consider adding specific skills relevant to your field (e.g., Python, SQL).")
        return suggestions if suggestions else ["Your resume looks solid! Tailor it to each job by emphasizing relevant skills."]

class LoganReid:
    """Employer Recruitment Agent"""
    def post_job(self, job_title, company, location, salary, description):
        """Simulate posting a job and provide feedback."""
        if all([job_title, company, location, salary, description]):
            return f"Job '{job_title}' for {company} posted successfully! Candidates will be screened and matched soon."
        return "Please fill out all job details to post the opening."

    def provide_recruitment_advice(self):
        """Offer recruitment advice."""
        return "To attract top talent, ensure your job description is clear and highlights benefits. Consider hosting a booth at our next job fair!"

class SophieBennett:
    """Interview Preparation Agent"""
    def get_common_questions(self):
        """Return a list of common interview questions."""
        return [
            "Tell me about yourself.",
            "What are your strengths and weaknesses?",
            "Why do you want to work for this company?",
            "Where do you see yourself in five years?",
            "Can you describe a challenging situation and how you handled it?"
        ]

    def get_preparation_tips(self, job_type):
        """Provide tailored interview tips based on job type."""
        if not job_type:
            return "Please select a job type to receive tailored interview tips."
        job_type = job_type.lower()
        if "software" in job_type or "engineer" in job_type:
            return "For tech roles, prepare for technical questions and coding challenges. Practice explaining your problem-solving process clearly."
        elif "nurse" in job_type or "health" in job_type:
            return "For healthcare roles, emphasize patient care experience and empathy. Be ready to discuss handling high-pressure situations."
        elif "warehouse" in job_type:
            return "For warehouse roles, highlight physical stamina and teamwork. Be prepared to discuss safety protocols and efficiency."
        elif "marketing" in job_type:
            return "For marketing roles, showcase creativity and data-driven decision-making. Prepare a portfolio of past campaigns if possible."
        else:
            return "For general roles, focus on clear communication, enthusiasm, and examples of past successes."

    def mock_interview_feedback(self, answer):
        """Provide feedback on a mock interview answer."""
        if not answer:
            return "Please provide an answer to receive feedback."
        feedback = []
        if len(answer.split()) < 20:
            feedback.append("Your answer is too brief. Try to elaborate with specific examples or details.")
        if not re.search(r"\b(result|achieved|succeeded|improved)\b", answer, re.IGNORECASE):
            feedback.append("Include outcomes or results to strengthen your response (e.g., 'This led to a 10% increase in efficiency').")
        if len(feedback) == 0:
            feedback.append("Good response! Ensure you tie it to the job's requirements for maximum impact.")
        return feedback

# Initialize Agents
emma = EmmaHarper(job_listings)
mason = MasonCole()
ava = AvaQuinn()
logan = LoganReid()
sophie = SophieBennett()

# App title and description
st.title("Career Workforce Center with AI Agents")
st.markdown("""
Welcome to the Career Workforce Center, powered by our AI agents:  
- **Emma Harper**: Your job matching expert  
- **Mason Cole**: Your career counseling guide  
- **Ava Quinn**: Your resume review specialist  
- **Sophie Bennett**: Your interview preparation coach  
- **Logan Reid**: Your recruitment partner  
""")

# Sidebar for user type selection
st.sidebar.header("Who Are You?")
user_type = st.sidebar.radio("Select your role:", ("Job Seeker", "Employer"))

# Main content based on user type
if user_type == "Job Seeker":
    st.header("Services for Job Seekers")
    
    # Tabs for different services
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Job Search", "Career Counseling", "Resume Review", "Interview Preparation", "Training Programs"])
    
    with tab1:
        st.subheader("Find a Job with Emma Harper")
        st.write("Search for jobs that match your skills and preferences.")
        keywords = st.text_input("Enter job title or keyword:", key="job_search_keywords")
        location_filter = st.selectbox("Filter by location:", ["All"] + job_listings["Location"].unique().tolist(), key="job_search_location")
        skills = st.text_input("Enter desired skills (e.g., Python, Nursing):", key="job_search_skills")
        
        if st.button("Search Jobs", key="search_jobs"):
            matched_jobs = emma.match_jobs(keywords, location_filter, skills)
            if matched_jobs.empty:
                st.warning("No jobs found. Try broadening your search terms.")
            else:
                st.dataframe(matched_jobs.drop(columns=['Score'] if 'Score' in matched_jobs.columns else []), use_container_width=True)
                if st.button("Apply for Selected Job", key="apply_job"):
                    st.success("Application submitted! Emma will notify you of next steps.")
    
    with tab2:
        st.subheader("Career Counseling with Mason Cole")
        st.write("Get personalized advice to achieve your career goals.")
        career_goal = st.text_area("What are your career goals?", key="career_goals")
        if st.button("Get Advice", key="get_advice"):
            advice = mason.provide_advice(career_goal)
            st.info(advice)
    
    with tab3:
        st.subheader("Resume Review with Ava Quinn")
        st.write("Paste your resume text for improvement suggestions.")
        resume_text = st.text_area("Paste your resume here:", key="resume_text")
        if st.button("Review Resume", key="review_resume"):
            suggestions = ava.review_resume(resume_text)
            for suggestion in suggestions:
                st.markdown(f"- {suggestion}")
    
    with tab4:
        st.subheader("Interview Preparation with Sophie Bennett")
        st.write("Prepare for your next interview with tailored tips and practice.")
        
        # Common Questions
        st.markdown("**Common Interview Questions**")
        questions = sophie.get_common_questions()
        for q in questions:
            st.markdown(f"- {q}")
        
        # Preparation Tips
        st.markdown("**Get Tailored Interview Tips**")
        job_type = st.text_input("Enter the job type you're preparing for (e.g., Software Engineer, Nurse):", key="job_type")
        if st.button("Get Interview Tips", key="get_interview_tips"):
            tips = sophie.get_preparation_tips(job_type)
            st.info(tips)
        
        # Mock Interview
        st.markdown("**Mock Interview Practice**")
        selected_question = st.selectbox("Choose a question to practice:", questions, key="mock_question")
        user_answer = st.text_area(f"Your answer to: '{selected_question}'", key="mock_answer")
        if st.button("Submit Answer for Feedback", key="submit_mock"):
            feedback = sophie.mock_interview_feedback(user_answer)
            for fb in feedback:
                st.markdown(f"- {fb}")
    
    with tab5:
        st.subheader("Explore Training Programs")
        st.write("Find training to gain skills for in-demand jobs.")
        st.dataframe(training_programs, use_container_width=True)
        selected_program = st.selectbox("Select a program to learn more:", training_programs["Program"], key="training_program")
        if st.button("Request Program Info", key="request_program"):
            st.success(f"Information about {selected_program} has been sent to your email.")

elif user_type == "Employer":
    st.header("Services for Employers")
    
    # Tabs for employer services
    tab1, tab2 = st.tabs(["Post a Job", "Recruitment Support"])
    
    with tab1:
        st.subheader("Post a Job with Logan Reid")
        st.write("Submit your job opening details.")
        job_title = st.text_input("Job Title", key="job_title")
        company = st.text_input("Company Name", key="company")
        location = st.text_input("Location", key="location")
        salary = st.text_input("Salary Range", key="salary")
        job_description = st.text_area("Job Description", key="job_description")
        
        if st.button("Post Job", key="post_job"):
            result = logan.post_job(job_title, company, location, salary, job_description)
            st.success(result) if "successfully" in result else st.error(result)
    
    with tab2:
        st.subheader("Recruitment Support with Logan Reid")
        st.write("Get help finding qualified candidates.")
        st.markdown("""
        - **Screening**: We review resumes to match your job requirements.
        - **Job Fairs**: Participate in our upcoming hiring events.
        - **Tax Credits**: Learn about incentives like the Work Opportunity Tax Credit.
        """)
        if st.button("Request Recruitment Advice", key="recruitment_advice"):
            advice = logan.provide_recruitment_advice()
            st.info(advice)

# Footer
st.markdown("---")
st.markdown("""
**Career Workforce Center** | Free services for job seekers and employers.  
Visit us at [CareerOneStop.org](https://www.careeronestop.org) or contact your local workforce agency.  
*Powered by AI agents, updated as of June 10, 2025.*
""")
