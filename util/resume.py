import os
import time
from typing import List
from config import Config
from util.skills import get_all_skills
from util.experience import get_all_experiences
from util.projects import get_all_projects
from pydantic import BaseModel
import re

def generate_resume(job_description: str) -> str:
    """
    Generate a resume based on the job description and candidate data.
    Uses a template and LLM to fill in the content, then saves to a text file.

    Args:
        job_description: The job description text.

    Returns:
        Path to the generated resume file.
    """
    print("Generating resume...")
    
    # Delay import to avoid circular dependency
    from util.llm import ChatLLM
    bot = ChatLLM()

    # Load resume template
    template_path = Config.RESUME_TEMPLATE_PATH
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()

    # Prepare system prompt to instruct the LLM
    system_prompt = (
        "You are a professional resume writer who writes resumes for software engineering. \
        Fill in the following template with the candidate's relevant information, tailored \
        to the job description. For filling out experience and projects, only use the name, \
        title, company, and dates in one line. Do not include any additional information."
    )
    
    # Get candidate data
    skills: List[str] = get_all_skills()
    experiences: List[str] = get_all_experiences()
    projects: List[str] = get_all_projects()
    
    # Prepare the user prompt with job description, skills, experiences, projects, and template
    prompt = (
        f"Job Description:\n{job_description}\n\n"
        f"Skills:\n{skills}\n\n"
        f"Experience:\n{experiences}\n\n"
        f"Projects:\n{projects}\n\n"
        f"Resume Template:\n{template}"
    )

    # Generate resume text 
    resume_text = bot.complete(
        prompt=prompt,
        model=Config.REASONING_MODEL,
        system_prompt=system_prompt
    )
    
    # Extract company and title from job description
    class schema(BaseModel):
        company: str
        job_title: str

    print("Extracting job info...")
    job_info = bot.complete(
        prompt=job_description,
        system_prompt="Extract the company name and job title from the job description. \
            Only output a single string in all caps, do not respond with anything else in your output. \
            Don't use any other punctuation. \
            Use _ instead of spaces.",
        model=Config.MINI_MODEL,
        temperature=0.0,
        schema=schema
    )
    
    # Determine output directory
    outdir = os.path.join(Config.CWD, 'documents')
    os.makedirs(outdir, exist_ok=True)
    sanitized_company = re.sub(r'[^0-9A-Za-z_]+', '_', job_info.company)
    sanitized_job_title = re.sub(r'[^0-9A-Za-z_]+', '_', job_info.job_title)
    filename = f"{sanitized_company}_{sanitized_job_title}_RESUME_{int(time.time())}.txt"
    outpath = os.path.join(outdir, filename)

    # Save the resume
    with open(outpath, 'w', encoding='utf-8') as f:
        f.write(resume_text)

    return outpath

