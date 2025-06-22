import unittest
import csv
import os
import tempfile
import shutil

from config import Config
import util.projects as projects
import util.experience as experience
import util.skills as skills

def write_csv(path, fieldnames, rows):
    """
    Helper to write CSV file with given headers and rows.
    """
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

class TestProjects(unittest.TestCase):
    def setUp(self):
        # Create temporary CSV file 
        self.tempdir = tempfile.mkdtemp()
        self.csv_path = os.path.join(self.tempdir, "projects.csv")
        fieldnames = [
            "ProjectName", "RelevantSkill1", "RelevantSkill2",
            "RelevantSkill3", "StartDate", "EndDate", "Description"
        ]
        rows = [
            {"ProjectName": "Alpha", "RelevantSkill1": "Py", "RelevantSkill2": "SQL", "RelevantSkill3": "", "StartDate": "01/2021", "EndDate": "06/2021", "Description": "Alpha desc"},
            {"ProjectName": "Beta",  "RelevantSkill1": "",   "RelevantSkill2": "",    "RelevantSkill3": "JS", "StartDate": "02/2022", "EndDate": "Present",      "Description": "Beta desc"},
        ]
        write_csv(self.csv_path, fieldnames, rows)
        # Patch config path
        self.orig_path = Config.PROJECTS_PATH
        Config.PROJECTS_PATH = self.csv_path

    def tearDown(self):
        # Restore and clean up
        Config.PROJECTS_PATH = self.orig_path
        shutil.rmtree(self.tempdir)

    def test_get_all_projects(self):
        data = projects.get_all_projects()
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["ProjectName"], "Alpha")

    def test_add_project(self):
        projects.add_project("Gamma", "A", "B", "C", "05/2023", "10/2023", "Gamma desc")
        data = projects.get_all_projects()
        self.assertEqual(len(data), 3)
        self.assertEqual(data[-1]["ProjectName"], "Gamma")

    def test_edit_project(self):
        projects.edit_project(1, project_name="Beta Updated", description="Updated desc")
        data = projects.get_all_projects()
        self.assertEqual(data[1]["ProjectName"], "Beta Updated")
        self.assertEqual(data[1]["Description"], "Updated desc")

    def test_delete_project(self):
        projects.delete_project(0)
        data = projects.get_all_projects()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["ProjectName"], "Beta")
    def test_add_project_empty_fields(self):
        # All fields are mandatory, empty fields should raise
        with self.assertRaises(ValueError):
            projects.add_project("", "RS1", "RS2", "RS3", "01/2021", "12/2021", "Desc")
        with self.assertRaises(ValueError):
            projects.add_project("Name", "", "RS2", "RS3", "01/2021", "12/2021", "Desc")

class TestExperience(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        self.csv_path = os.path.join(self.tempdir, "experience.csv")
        fieldnames = [
            "Company", "Title", "Location", "StartDate",
            "EndDate", "BulletPt1", "BulletPt2", "BulletPt3"
        ]
        rows = [
            {"Company": "CompA", "Title": "Dev", "Location": "NY", "StartDate": "01/2020", "EndDate": "12/2020", "BulletPt1": "Did X", "BulletPt2": "",      "BulletPt3": ""},
            {"Company": "CompB", "Title": "Eng", "Location": "SF", "StartDate": "03/2021", "EndDate": "Present",      "BulletPt1": "",      "BulletPt2": "Did Y", "BulletPt3": ""},
        ]
        write_csv(self.csv_path, fieldnames, rows)
        self.orig_path = Config.EXPERIENCE_PATH
        Config.EXPERIENCE_PATH = self.csv_path

    def tearDown(self):
        Config.EXPERIENCE_PATH = self.orig_path
        shutil.rmtree(self.tempdir)

    def test_get_all_experiences(self):
        data = experience.get_all_experiences()
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["Company"], "CompA")

    def test_add_experience(self):
        experience.add_experience("CompC", "Mgr", "LA", "01/2022", "12/2022", "Pt1", "Pt2", "Pt3")
        data = experience.get_all_experiences()
        self.assertEqual(len(data), 3)
        self.assertEqual(data[-1]["Company"], "CompC")

    def test_edit_experience(self):
        experience.edit_experience(0, title="DevOps", bullet_pt1="New Pt1")
        data = experience.get_all_experiences()
        self.assertEqual(data[0]["Title"], "DevOps")
        self.assertEqual(data[0]["BulletPt1"], "New Pt1")

    def test_delete_experience(self):
        experience.delete_experience(1)
        data = experience.get_all_experiences()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["Company"], "CompA")
    def test_add_experience_empty_fields(self):
        # All fields are mandatory, empty fields should raise
        with self.assertRaises(ValueError):
            experience.add_experience("", "Title", "Loc", "01/2020", "12/2020", "B1", "B2", "B3")
        with self.assertRaises(ValueError):
            experience.add_experience("Comp", "", "Loc", "01/2020", "12/2020", "B1", "B2", "B3")
    def test_add_experience_optional_bullets(self):
        # Bullet points are optional and may be empty
        experience.add_experience("CompD", "Lead", "LA", "04/2021", "10/2021", "", "", "")
        data = experience.get_all_experiences()
        self.assertEqual(len(data), 3)
        last = data[-1]
        self.assertEqual(last["Company"], "CompD")
        self.assertEqual(last["BulletPt1"], "")
        self.assertEqual(last["BulletPt2"], "")
        self.assertEqual(last["BulletPt3"], "")

class TestSkills(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        self.csv_path = os.path.join(self.tempdir, "skills.csv")
        fieldnames = ["Skill", "Category"]
        rows = [
            {"Skill": "Python",       "Category": "Programming Languages"},
            {"Skill": "Communication", "Category": "Other"},
        ]
        write_csv(self.csv_path, fieldnames, rows)
        self.orig_path = Config.SKILLS_PATH
        Config.SKILLS_PATH = self.csv_path

    def tearDown(self):
        Config.SKILLS_PATH = self.orig_path
        shutil.rmtree(self.tempdir)

    def test_get_all_skills(self):
        data = skills.get_all_skills()
        self.assertEqual(len(data), 2)
        self.assertEqual(data[1]["Skill"], "Communication")

    def test_get_skills_by_category(self):
        data = skills.get_skills_by_category("Programming Languages")
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["Skill"], "Python")

    def test_add_skill(self):
        skills.add_skill("Leadership", "Other")
        data = skills.get_all_skills()
        self.assertEqual(len(data), 3)
        self.assertEqual(data[-1]["Skill"], "Leadership")
        self.assertEqual(data[-1]["Category"], "Other")

    def test_edit_skill(self):
        # Change to a valid allowed category
        skills.edit_skill(1, skill="Communication Updated", category="Frameworks/Libraries")
        data = skills.get_all_skills()
        self.assertEqual(data[1]["Skill"], "Communication Updated")
        self.assertEqual(data[1]["Category"], "Frameworks/Libraries")

    def test_delete_skill(self):
        skills.delete_skill(0)
        data = skills.get_all_skills()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["Skill"], "Communication")
    def test_add_skill_empty_fields(self):
        # Skill and category are mandatory
        with self.assertRaises(ValueError):
            skills.add_skill("", "Category")
        with self.assertRaises(ValueError):
            skills.add_skill("Skill", "")
    def test_add_skill_invalid_category(self):
        # Category must be one of allowed
        with self.assertRaises(ValueError):
            skills.add_skill("Go", "Language")
    def test_get_skills_by_category_empty(self):
        # Category filter must be non-empty
        with self.assertRaises(ValueError):
            skills.get_skills_by_category("")
    def test_get_skills_by_category_invalid(self):
        # Category must be one of allowed
        with self.assertRaises(ValueError):
            skills.get_skills_by_category("InvalidCategory")
    def test_edit_skill_invalid_category(self):
        # Editing to invalid category should raise
        with self.assertRaises(ValueError):
            skills.edit_skill(0, category="InvalidCategory")

if __name__ == "__main__":
    unittest.main()