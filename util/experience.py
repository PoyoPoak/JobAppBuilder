import csv
import os
from config import Config

"""CRUD operations for experience entries."""

def get_all_experiences():
    """
    Retrieves all experience entries from the CSV.

    Returns:
        List[dict]: list of experience entries, keys are CSV headers.

    Raises:
        FileNotFoundError: if the CSV file does not exist.
    """
    path = Config.EXPERIENCE_PATH
    if not os.path.exists(path):
        raise FileNotFoundError(f"Experience file not found at {path}")
    with open(path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)

def add_experience(company: str, title: str, location: str, start_date: str,
                   end_date: str, bullet_pt1: str, bullet_pt2: str, bullet_pt3: str) -> None:
    """
    Adds a new experience entry to the CSV.

    Mandatory parameters:
        company (str), title (str), location (str), start_date (str)
    Optional parameters:
        end_date (str), bullet_pt1 (str), bullet_pt2 (str), bullet_pt3 (str)

    Raises:
        FileNotFoundError: if the CSV file does not exist.
        ValueError: if any mandatory field is empty.
    """
    # All fields are mandatory and must be non-empty strings
    required = [company, title, location, start_date, end_date, bullet_pt1, bullet_pt2, bullet_pt3]
    if not all(isinstance(x, str) and x.strip() for x in required):
        raise ValueError("All experience fields must be non-empty strings")
    path = Config.EXPERIENCE_PATH
    if not os.path.exists(path):
        raise FileNotFoundError(f"Experience file not found at {path}")
    row = {
        "Company": company.strip(),
        "Title": title.strip(),
        "Location": location.strip(),
        "StartDate": start_date.strip(),
        "EndDate": end_date.strip(),
        "BulletPt1": bullet_pt1.strip(),
        "BulletPt2": bullet_pt2.strip(),
        "BulletPt3": bullet_pt3.strip(),
    }
    with open(path, "a", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["Company", "Title", "Location", "StartDate", "EndDate", "BulletPt1", "BulletPt2", "BulletPt3"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow(row)

def edit_experience(index: int, company: str = None, title: str = None, location: str = None,
                    start_date: str = None, end_date: str = None,
                    bullet_pt1: str = None, bullet_pt2: str = None, bullet_pt3: str = None) -> None:
    """
    Edits an existing experience entry by index (0-based).

    Mandatory parameter:
        index (int)
    Optional parameters:
        company, title, location, start_date, end_date, bullet_pt1, bullet_pt2, bullet_pt3

    Raises:
        FileNotFoundError: if the CSV file does not exist.
        IndexError: if the index is out of range.
        ValueError: if provided field values are invalid.
    """
    path = Config.EXPERIENCE_PATH
    if not os.path.exists(path):
        raise FileNotFoundError(f"Experience file not found at {path}")
    if not isinstance(index, int):
        raise ValueError("index must be an integer")
    with open(path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)
        fieldnames = reader.fieldnames or []
    if index < 0 or index >= len(rows):
        raise IndexError(f"Index {index} is out of range")
    updates = {
        "Company": company,
        "Title": title,
        "Location": location,
        "StartDate": start_date,
        "EndDate": end_date,
        "BulletPt1": bullet_pt1,
        "BulletPt2": bullet_pt2,
        "BulletPt3": bullet_pt3,
    }
    for key, value in updates.items():
        if value is not None:
            if not isinstance(value, str):
                raise ValueError(f"{key} must be a string")
            rows[index][key] = value.strip()
    with open(path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def delete_experience(index: int) -> None:
    """
    Deletes an experience entry by index (0-based).

    Mandatory parameter:
        index (int)

    Raises:
        FileNotFoundError: if the CSV file does not exist.
        IndexError: if the index is out of range.
    """
    path = Config.EXPERIENCE_PATH
    if not os.path.exists(path):
        raise FileNotFoundError(f"Experience file not found at {path}")
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