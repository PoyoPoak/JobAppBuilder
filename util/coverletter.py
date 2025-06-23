import os
import time
import json
import re
from config import Config
from util.skills import get_all_skills
from util.experience import get_all_experiences
from util.projects import get_all_projects
from pydantic import BaseModel


def generate_cover_letter_outlines(job_description: str, count: int = 3) -> list[str]:
    """
    Produce `count` high-level bullet outlines tailored to the job description
    and our skills/experience/projects. Returns a list of outline strings.
    """
    from util.llm import ChatLLM
    bot = ChatLLM()

    skills = get_all_skills()
    exps = get_all_experiences()
    projs = get_all_projects()

    system_prompt = f"You are a professional cover-letter writer. \
        Given the job description and the candidate's background, propose {count} distinct outlines for the body of a cover letter. \
        Return only a JSON array of strings, each string an outline in bullet form. \
        The tone of the letter should be professional, confident, and competant. Not overly excited. \
        The letter is addressing the hiring manager and potentially the team. \
        There should be a focus on the candidate's skills, experience, and projects relevant to the job description. \
        Mention the desire for career and professional growth. \
        Do not open with expressions like 'I am excited to apply' or 'I am thrilled to express my enthusiasm' or similar. \
        The length of the cover letter is intended to be one page, 200-300 words. \
        Do not use Paragraphs, use bullet points for the outlines."

    user_prompt = (
        f"Job Description:\n{job_description}\n\n"
        f"Skills:\n{skills}\n\n"
        f"Experience:\n{exps}\n\n"
        f"Projects:\n{projs}"
    )

    class schema(BaseModel):
        outlines: list[str]

    resp = bot.complete(
        prompt=user_prompt,
        system_prompt=system_prompt,
        model=Config.REASONING_MODEL,
        schema=schema,
    )
    
    return resp.outlines


def select_best(cover_letters: list[str], 
                job_description: str,
                count: int = 1) -> list[str]:
    """
    Given a list of cover letters and the job description, pick the best one.
    Returns a list of strings (the chosen outline broken into bullet points).
    """
    if len(cover_letters) == 1:
        return cover_letters
    
    from util.llm import ChatLLM
    bot = ChatLLM()

    system_prompt = (
        f"You are a professional cover letter writer and career development professional specializing in computer science careers. \
        From the provided cover letters and job description, choose the {count} most fitting cover letters. \
        Return only a JSON array of strings."
    )

    user_prompt = (
        f"Cover Letters:\n{cover_letters}\n\n"
        f"Job Description:\n{job_description}"
    )

    class schema(BaseModel):
        cover_letters: list[str]

    resp = bot.complete(
        prompt=user_prompt,
        system_prompt=system_prompt,
        model=Config.REASONING_MODEL,
        schema=schema
    )
    
    return resp.cover_letters


def generate_cover_letter(outline: str,
                          job_description: str) -> str:
    """
    Expand a single outline into a full cover letter draft (body only).
    """
    from util.llm import ChatLLM
    bot = ChatLLM()

    skills = get_all_skills()
    exps = get_all_experiences()
    projs = get_all_projects()

    system_prompt = (
        "You are a professional cover-letter writer. \
        Using the outline below and the candidate's context, write a polished cover-letter body. \
        The tone of the letter should be professional, confident, and competant. Not overly excited. \
        The letter is addressing the hiring manager and potentially the team. \
        There should be a focus on the candidate's skills, experience, and projects relevant to the job description. \
        Mention the desire for career and professional growth. \
        Do not open with expressions like 'I am excited to apply' or 'I am thrilled to express my enthusiasm' or similar."
    )

    user_prompt = (
        f"Outline:\n{outline}\n\n"
        f"Job Description:\n{job_description}\n\n"
        f"Skills:\n{skills}\n\n"
        f"Experience:\n{exps}\n\n"
        f"Projects:\n{projs}"
    )

    resp = bot.complete(
        prompt=user_prompt,
        system_prompt=system_prompt,
        model=Config.STANDARD_MODEL,
        temperature=0.5
    )

    return resp


def detect_ai_content(cover_letter: str) -> dict:
    """
    Analyze the cover letter and return a JSON object of numeric AI‐detection scores.
    """
    from util.llm import ChatLLM
    bot = ChatLLM()

    system_prompt = (
        "You are an AI-detection assistant. \
        Rate the following cover letter on a scale from 0 to 100 for likelihood of AI generation. \
        Return only a JSON object the score and feedback."
    )

    user_prompt = f"Cover Letter:\n{cover_letter}"

    class schema(BaseModel):
        score: int
        feedback: str

    resp = bot.complete(
        prompt=user_prompt,
        system_prompt=system_prompt,
        model=Config.STANDARD_MODEL,
        temperature=0.0,
        schema=schema
    )
    
    return resp.score, resp.feedback


def revise_cover_letter(cover_letter: str,
                        feedback: str,
                        job_description: str) -> str:
    """
    Given AI-detection feedback, ask the LLM to revise the letter to lower AI-detectable signals.
    """
    from util.llm import ChatLLM
    bot = ChatLLM()

    system_prompt = (
        "You are a professional cover-letter writer. \
        You are a very critical editor who revises cover letters to reduce AI-detection scores and sound less generic. \
        Revise the letter to address the AI-detection feedback below. \
        Reduce formulaic repetitive patterns, words, and anything common with AI while preserving content. \
        It should sound natural and human-like, not overly formal or robotic. \
        Should sound like a recent college graduate wrote this without harming quality. \
        Only output the revised letter, do not include any other text."
    )

    user_prompt = (
        f"Original Letter:\n{cover_letter}\n\n"
        f"Feedback:\n{feedback}\n\n"
        f"Job Description:\n{job_description}"
    )

    resp = bot.complete(
        prompt=user_prompt,
        system_prompt=system_prompt,
        model=Config.REASONING_MODEL,
    )
    
    return resp


def save_cover_letter(cover_letter: str, job_info: str) -> str:
    """
    Save the final letter to ./documents with timestamped filename.
    """
    outdir = os.path.join(Config.CWD, "documents")
    os.makedirs(outdir, exist_ok=True)
    filename = f"{job_info}_COVERLETTER_{int(time.time())}.txt"
    path = os.path.join(outdir, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(cover_letter)

    return path


def create_cover_letter(job_description: str, count: int = 1) -> list[str]:
    """
    Orchestrate the full pipeline and return a list of file paths.
    """
    print("Generating cover letter...")
    
    # Extract company and title from job description
    from util.llm import ChatLLM
    bot = ChatLLM()

    print("Extracting job info...")
    job_info = bot.complete(
        prompt=job_description,
        system_prompt="Extract the company name and job title from the job description. \
            Only output a single string in the format \"Company: [COMPANYNAME], Job Title: [JOBTITLE]\" in all caps, do not respond with anything else in your output. \
            Don't use any other punctuation. \
            This should sound like an actual letter, not some canned marketing flyer. \
            If the any part contains spaces, use a _ instead of a space. \
            Insert the company name job title respectively as [COMPANYNAME] and [JOBTITLE]. \
            Remember to use a comma and a space between the company name and job title as shown in the format.",
        model=Config.MINI_MODEL,
        temperature=0.0
    )

    # Add job_info to the job description for context at the start
    job_description = f"Job Info: {job_info}\n\n{job_description}"

    # Generate outlines as a json array of strings
    print("Generating outlines...")
    outlines = generate_cover_letter_outlines(job_description)

    # For each outline, generate a cover letter, and check the AI-detection score on each one, revise if necessary
    print("Generating cover letter text...")
    cover_letters = [] 
    for outline in outlines:
        # Generate the cover letter draft
        cover_letter = generate_cover_letter(outline, job_description)

        # Check AI-detection score
        score, feedback = detect_ai_content(cover_letter)

        # If score is high, revise the letter
        if score > 10:
            print(f"Revising letter with score {score}...")
            cover_letter = revise_cover_letter(cover_letter, feedback, job_description)
            rescore, feedback = detect_ai_content(cover_letter)
            print(f"Revised letter score: {rescore}...")

        # Add cover letter to the list
        cover_letters.append(cover_letter)
        
    # Select the best cover letter(s)
    print("Selecting best cover letter(s)...")
    best = select_best(cover_letters, job_description, count)
    
    print("Saving cover letters...")
    for letter in best:
        sanitized = re.sub(r'[^0-9A-Za-z_]+', '_', job_info)
        filename = f"{sanitized}_COVERLETTER_{int(time.time())}.txt"
        path = os.path.join(Config.DOCUMENTS_PATH, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(letter)
        print(f"Saved cover letter to {path}")
