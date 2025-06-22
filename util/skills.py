import csv
import os
from config import Config

# Allowed categories for skills
ALLOWED_CATEGORIES = [
    "Programming Languages",
    "Frameworks/Libraries",
    "Platforms/Tools",
    "Other",
]

"""CRUD operations for skills entries."""

def get_all_skills() -> list[dict]:
    """
    Retrieves all skills entries from the CSV.

    Returns:
        List[dict]: list of skill entries, keys are CSV headers.

    Raises:
        FileNotFoundError: if the CSV file does not exist.
    """
    path = Config.SKILLS_PATH
    if not os.path.exists(path):
        raise FileNotFoundError(f"Skills file not found at {path}")
    with open(path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)

def get_skills_by_category(category: str) -> list[dict]:
    """
    Retrieves skills filtered by category.

    Mandatory parameter:
        category (str)

    Raises:
        FileNotFoundError: if the CSV file does not exist.
        ValueError: if category is empty.
    """
    if not isinstance(category, str) or not category.strip():
        raise ValueError("category must be a non-empty string")
    cat = category.strip()
    if cat not in ALLOWED_CATEGORIES:
        raise ValueError(f"category must be one of {ALLOWED_CATEGORIES}")
    skills = get_all_skills()
    return [row for row in skills if row.get("Category") == cat]

def add_skill(skill: str, category: str) -> None:
    """
    Adds a new skill entry to the CSV.

    Mandatory parameters:
        skill (str), category (str)

    Raises:
        FileNotFoundError: if the CSV file does not exist.
        ValueError: if any mandatory field is empty.
    """
    # Both skill and category are mandatory and must be non-empty strings
    if not all(isinstance(x, str) and x.strip() for x in [skill, category]):
        raise ValueError("skill and category are required and must be non-empty strings")
    cat = category.strip()
    if cat not in ALLOWED_CATEGORIES:
        raise ValueError(f"category must be one of {ALLOWED_CATEGORIES}")
    path = Config.SKILLS_PATH
    if not os.path.exists(path):
        raise FileNotFoundError(f"Skills file not found at {path}")
    row = {"Skill": skill.strip(), "Category": cat}
    with open(path, "a", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["Skill", "Category"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow(row)

def edit_skill(index: int, skill: str = None, category: str = None) -> None:
    """
    Edits an existing skill entry by index (0-based).

    Mandatory parameter:
        index (int)
    Optional parameters:
        skill (str), category (str)

    Raises:
        FileNotFoundError: if the CSV file does not exist.
        IndexError: if the index is out of range.
        ValueError: if provided values are invalid.
    """
    path = Config.SKILLS_PATH
    if not os.path.exists(path):
        raise FileNotFoundError(f"Skills file not found at {path}")
    if not isinstance(index, int):
        raise ValueError("index must be an integer")
    with open(path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)
        fieldnames = reader.fieldnames or []
    if index < 0 or index >= len(rows):
        raise IndexError(f"Index {index} is out of range")
    if skill is not None:
        if not isinstance(skill, str):
            raise ValueError("skill must be a string")
        rows[index]["Skill"] = skill.strip()
    if category is not None:
        if not isinstance(category, str):
            raise ValueError("category must be a string")
        cat = category.strip()
        if cat not in ALLOWED_CATEGORIES:
            raise ValueError(f"category must be one of {ALLOWED_CATEGORIES}")
        rows[index]["Category"] = cat
    with open(path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def delete_skill(index: int) -> None:
    """
    Deletes a skill entry by index (0-based).

    Mandatory parameter:
        index (int)

    Raises:
        FileNotFoundError: if the CSV file does not exist.
        IndexError: if the index is out of range.
    """
    path = Config.SKILLS_PATH
    if not os.path.exists(path):
        raise FileNotFoundError(f"Skills file not found at {path}")
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