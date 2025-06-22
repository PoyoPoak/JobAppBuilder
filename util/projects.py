import csv
import os
import re
from config import Config

# Date must be MM-YYYY or literal 'Present'
def _validate_date(date_str: str) -> None:
    if date_str != "Present" and not re.match(r"^(0[1-9]|1[0-2])/[0-9]{4}$", date_str):
        raise ValueError("Date must be in MM/YYYY format or 'Present'")

"""CRUD operations for project entries."""

def get_all_projects() -> list[dict]:
    """
    Retrieves all project entries from the CSV.

    Returns:
        List[dict]: list of project entries, keys are CSV headers.

    Raises:
        FileNotFoundError: if the CSV file does not exist.
    """
    path = Config.PROJECTS_PATH
    if not os.path.exists(path):
        raise FileNotFoundError(f"Projects file not found at {path}")
    with open(path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)

def add_project(project_name: str, relevant_skill1: str, relevant_skill2: str, relevant_skill3: str,
                start_date: str, end_date: str, description: str) -> None:
    """
    Adds a new project entry to the CSV.

    Parameters:
        project_name (str): name of the project.
        relevant_skill1 (str): primary relevant skill.
        relevant_skill2 (str): secondary relevant skill.
        relevant_skill3 (str): tertiary relevant skill.
        start_date (str): start date in MM-YYYY or 'Present'.
        end_date (str): end date in MM-YYYY or 'Present'.
        description (str): project description.

    Raises:
        FileNotFoundError: if the CSV file does not exist.
        ValueError: if any mandatory field is empty.
    """
    # All fields are mandatory and must be non-empty strings
    required = [project_name, relevant_skill1, relevant_skill2, relevant_skill3, start_date, end_date, description]
    if not all(isinstance(x, str) and x.strip() for x in required):
        raise ValueError("All project fields must be non-empty strings")
    path = Config.PROJECTS_PATH
    if not os.path.exists(path):
        raise FileNotFoundError(f"Projects file not found at {path}")
    row = {
        "ProjectName": project_name.strip(),
        "RelevantSkill1": relevant_skill1.strip(),
        "RelevantSkill2": relevant_skill2.strip(),
        "RelevantSkill3": relevant_skill3.strip(),
        "StartDate": start_date.strip(),
        "EndDate": end_date.strip(),
        "Description": description.strip(),
    }
    # Validate date fields
    _validate_date(row["StartDate"])
    _validate_date(row["EndDate"])
    with open(path, "a", newline="", encoding="utf-8") as csvfile:
        fieldnames = [
            "ProjectName", "RelevantSkill1", "RelevantSkill2",
            "RelevantSkill3", "StartDate", "EndDate", "Description"
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow(row)

def edit_project(index: int, project_name: str = None, relevant_skill1: str = None,
                 relevant_skill2: str = None, relevant_skill3: str = None,
                 start_date: str = None, end_date: str = None, description: str = None) -> None:
    """
    Edits an existing project entry by index (0-based).

    Mandatory parameter:
        index (int)
    Optional parameters:
        project_name, relevant_skill1, relevant_skill2, relevant_skill3,
        start_date, end_date, description

    Raises:
        FileNotFoundError: if the CSV file does not exist.
        IndexError: if the index is out of range.
        ValueError: if provided values are invalid.
    """
    path = Config.PROJECTS_PATH
    if not os.path.exists(path):
        raise FileNotFoundError(f"Projects file not found at {path}")
    if not isinstance(index, int):
        raise ValueError("index must be an integer")
    with open(path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)
        fieldnames = reader.fieldnames or []
    if index < 0 or index >= len(rows):
        raise IndexError(f"Index {index} is out of range")
    updates = {
        "ProjectName": project_name,
        "RelevantSkill1": relevant_skill1,
        "RelevantSkill2": relevant_skill2,
        "RelevantSkill3": relevant_skill3,
        "StartDate": start_date,
        "EndDate": end_date,
        "Description": description,
    }
    for key, value in updates.items():
        if value is not None:
            if not isinstance(value, str):
                raise ValueError(f"{key} must be a string")
            val = value.strip()
            # validate date fields
            if key in ("StartDate", "EndDate"):
                _validate_date(val)
            rows[index][key] = val
    with open(path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def delete_project(index: int) -> None:
    """
    Deletes a project entry by index (0-based).

    Mandatory parameter:
        index (int)

    Raises:
        FileNotFoundError: if the CSV file does not exist.
        IndexError: if the index is out of range.
    """
    path = Config.PROJECTS_PATH
    if not os.path.exists(path):
        raise FileNotFoundError(f"Projects file not found at {path}")
    if not isinstance(index, int):
        raise ValueError("index must be an integer")
    with open(path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)
        fieldnames = reader.fieldnames or []
    if index < 0 or index >= len(rows):
        raise IndexError(f"Index {index} is out of range")
    rows.pop(index)
    with open(path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)