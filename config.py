import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # Paths to data and resources
    CWD = os.getcwd()
    EXPERIENCE_PATH = os.path.join(CWD, "data", "experience.csv")
    PROJECTS_PATH = os.path.join(CWD, "data", "projects.csv")
    SKILLS_PATH = os.path.join(CWD, "data", "skills.csv")
    JOBS_PATH = os.path.join(CWD, "data", "jobs.csv")
    RESUME_TEMPLATE_PATH = os.path.join(CWD, "resources", "resume_template.txt")
    RUBRIC_PATH = os.path.join(CWD, "resources", "ai_detection_rubric.txt")
    DOCUMENTS_PATH = os.path.join(CWD, "documents")
    
    # LLM model names
    REASONING_MODEL = "o4-mini"
    STANDARD_MODEL = "gpt-4o"
    MINI_MODEL = "gpt-4.1-nano"

    # JSON-Schema specs for LLM function tools
    TOOL_SPECS = [
        {
            "name": "generate_resume",
            "description": "Generate a resume based on job description and candidate data.",
            "type": "function",
            "parameters": {
                "type": "object",
                "properties": {
                    "job_description": {"type": "string", "description": "Job description text"}
                },
                "required": ["job_description"]
            }
        },
        {
            "name": "get_all_experiences",
            "description": "Retrieves all experience entries from the CSV.",
            "type": "function",
            "parameters": {"type": "object", "properties": {}, "required": []}
        },
        {
            "name": "add_experience",
            "description": "Adds a new experience entry to the CSV.",
            "type": "function",
            "parameters": {
                "type": "object",
                "properties": {
                    "company": {"type": "string", "description": "Company name"},
                    "title": {"type": "string", "description": "Job title"},
                    "location": {"type": "string", "description": "Location"},
                    "start_date": {"type": "string", "description": "Start date MM/YYYY or 'Present'"},
                    "end_date": {"type": "string", "description": "End date MM/YYYY or 'Present'"},
                    "bullet_pt1": {"type": "string", "description": "Bullet point 1"},
                    "bullet_pt2": {"type": "string", "description": "Bullet point 2"},
                    "bullet_pt3": {"type": "string", "description": "Bullet point 3"}
                },
                "required": ["company", "title", "location", "start_date", "end_date", "bullet_pt1", "bullet_pt2", "bullet_pt3"]
            }
        },
        {
            "name": "edit_experience",
            "description": "Edits an existing experience entry by index (0-based).",
            "type": "function",
            "parameters": {
                "type": "object",
                "properties": {
                    "index": {"type": "integer", "description": "Index of the experience entry to edit"},
                    "company": {"type": "string", "description": "Company name"},
                    "title": {"type": "string", "description": "Job title"},
                    "location": {"type": "string", "description": "Location"},
                    "start_date": {"type": "string", "description": "Start date MM/YYYY or 'Present'"},
                    "end_date": {"type": "string", "description": "End date MM/YYYY or 'Present'"},
                    "bullet_pt1": {"type": "string", "description": "Bullet point 1"},
                    "bullet_pt2": {"type": "string", "description": "Bullet point 2"},
                    "bullet_pt3": {"type": "string", "description": "Bullet point 3"}
                },
                "required": ["index"]
            }
        },
        {
            "name": "delete_experience",
            "description": "Deletes an experience entry by index (0-based).",
            "type": "function",
            "parameters": {
                "type": "object",
                "properties": {"index": {"type": "integer", "description": "Index of the experience entry to delete"}},
                "required": ["index"]
            }
        },
        {
            "name": "get_all_projects",
            "description": "Retrieves all project entries from the CSV.",
            "type": "function",
            "parameters": {"type": "object", "properties": {}, "required": []}
        },
        {
            "name": "add_project",
            "description": "Adds a new project entry to the CSV.",
            "type": "function",
            "parameters": {
                "type": "object",
                "properties": {
                    "project_name": {"type": "string", "description": "Name of the project"},
                    "relevant_skill1": {"type": "string", "description": "Primary relevant skill"},
                    "relevant_skill2": {"type": "string", "description": "Secondary relevant skill"},
                    "relevant_skill3": {"type": "string", "description": "Tertiary relevant skill"},
                    "start_date": {"type": "string", "description": "Start date MM/YYYY or 'Present'"},
                    "end_date": {"type": "string", "description": "End date MM/YYYY or 'Present'"},
                    "description": {"type": "string", "description": "Project description"}
                },
                "required": ["project_name", "relevant_skill1", "relevant_skill2", "relevant_skill3", "start_date", "end_date", "description"]
            }
        },
        {
            "name": "edit_project",
            "description": "Edits an existing project entry by index (0-based).",
            "type": "function",
            "parameters": {
                "type": "object",
                "properties": {
                    "index": {"type": "integer", "description": "Index of the project entry to edit"},
                    "project_name": {"type": "string", "description": "Name of the project"},
                    "relevant_skill1": {"type": "string", "description": "Primary relevant skill"},
                    "relevant_skill2": {"type": "string", "description": "Secondary relevant skill"},
                    "relevant_skill3": {"type": "string", "description": "Tertiary relevant skill"},
                    "start_date": {"type": "string", "description": "Start date MM/YYYY or 'Present'"},
                    "end_date": {"type": "string", "description": "End date MM/YYYY or 'Present'"},
                    "description": {"type": "string", "description": "Project description"}
                },
                "required": ["index"]
            }
        },
        {
            "name": "delete_project",
            "description": "Deletes a project entry by index (0-based).",
            "type": "function",
            "parameters": {
                "type": "object",
                "properties": {"index": {"type": "integer", "description": "Index of the project entry to delete"}},
                "required": ["index"]
            }
        },
        {
            "name": "get_all_skills",
            "description": "Retrieves all skills entries from the CSV.",
            "type": "function",
            "parameters": {"type": "object", "properties": {}, "required": []}
        },
        {
            "name": "get_skills_by_category",
            "description": "Retrieves skills filtered by category. There are only the following categories such as 'Programming Languages', 'Frameworks/Libraries', 'Platforms/Tools', 'Other'",
            "type": "function",
            "parameters": {
                "type": "object",
                "properties": {
                    "category": {"type": "string", "description": "Skill category to filter by"}
                },
                "required": ["category"]
            }
        },
        {
            "name": "add_skill",
            "description": "Adds a new skill entry to the CSV. The skill must be unique in its name. Categories include 'Programming Languages', 'Frameworks/Libraries', 'Platforms/Tools', 'Other'.",
            "type": "function",
            "parameters": {
                "type": "object",
                "properties": {
                    "skill": {"type": "string", "description": "Name of the skill"},
                    "category": {"type": "string", "description": "Category of the skill"}
                },
                "required": ["skill", "category"]
            }
        },
        {
            "name": "edit_skill",
            "description": "Edits an existing skill entry by index (0-based). The skill must be unique in its name. Categories include 'Programming Languages', 'Frameworks/Libraries', 'Platforms/Tools', 'Other'.",
            "type": "function",
            "parameters": {
                "type": "object",
                "properties": {
                    "index": {"type": "integer", "description": "Index of the skill entry to edit"},
                    "skill": {"type": "string", "description": "Name of the skill"},
                    "category": {"type": "string", "description": "Category of the skill"}
                },
                "required": ["index"]
            }
        },
        {
            "name": "delete_skill",
            "description": "Deletes a skill entry by index (0-based).",
            "type": "function",
            "parameters": {
                "type": "object",
                "properties": {"index": {"type": "integer", "description": "Index of the skill entry to delete"}},
                "required": ["index"]
            }
        },
        {
            "name": "create_cover_letter",
            "description": "Orchestrate outline generation, drafting, detection, revision, and saving of cover letters.",
            "type": "function",
            "parameters": {
                "type": "object",
                "properties": {
                    "job_description": {"type": "string", "description": "Job description text"},
                    "count": {"type": "integer", "description": "Number of cover letters to create"}
                },
                "required": ["job_description"]
            }
        }
    ]