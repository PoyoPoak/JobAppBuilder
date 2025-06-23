import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    CWD = os.getcwd()
    EXPERIENCE_PATH = os.path.join(CWD, "data", "experience.csv")
    PROJECTS_PATH = os.path.join(CWD, "data", "projects.csv")
    SKILLS_PATH = os.path.join(CWD, "data", "skills.csv")
    JOBS_PATH = os.path.join(CWD, "data", "jobs.csv")
    RESUME_TEMPLATE_PATH = os.path.join(CWD, "resources", "resume_template.txt")
    REASONING_MODEL = "o4-mini"
    STANDARD_MODEL = "gpt-4o"
    MINI_MODEL = "gpt-4.1-nano"