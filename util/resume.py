import os
import time
from typing import List, Dict, Optional
from config import Config
from util.llm import ChatLLM

def generate_resume(job_description: str,
                    skills: List[Dict[str, str]],
                    experiences: List[Dict[str, str]],
                    projects: List[Dict[str, str]],
                    ) -> str:
    """
    Generate a resume based on the job description and candidate data.
    Uses a template and LLM to fill in the content, then saves to a text file.

    Args:
        job_description: The job description text.
        skills: List of skill dictionaries.
        experiences: List of experience dictionaries.
        projects: List of project dictionaries.

    Returns:
        Path to the generated resume file.
    """
    print("Generating resume...")
    
    # Initialize LLM client
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
    job_info = bot.complete(
        prompt=job_description,
        model=Config.MINI_MODEL,
        system_prompt="Extract the company name and job title from the job description. Only output a single string in the format \"COMPANYNAME_TITLE\" in all caps, do not respond with anything else in your output.",
        temperature=0.0
    )

    # Determine output directory
    outdir = os.path.join(Config.CWD, 'documents')
    os.makedirs(outdir, exist_ok=True)
    filename = f"{job_info}_RESUME_{int(time.time())}.txt"
    outpath = os.path.join(outdir, filename)

    # Save the resume
    with open(outpath, 'w', encoding='utf-8') as f:
        f.write(resume_text)

    return outpath

