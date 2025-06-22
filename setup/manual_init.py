from util import projects, experience, skills

def main():
    projects.add_project(
        "RealDoc",
        "Python",
        "AWS",
        "SQL",
        "07/2024",
        "Present",
        "Implemented payment processing, API unit tests, and bug fixes for a web based automation used in real estate continuing education certificates with active users saving +300 hours a month."
    )
    projects.add_project(
        "PDF Overlay Tool",
        "Python",
        "Pyinstaller",
        "Tkinter",
        "05/2025",
        "05/2025",
        "Reduced manual PDF work by over 80% for a local business by creating a custom Windows executable for batch PDF combination and overlay."
    )
    projects.add_project(
        "Documentation Retrieval-Augmented Generation System",
        "Python",
        "C#",
        "MySQL",
        "03/2025",
        "03/2025",
        "Improved developer efficiency by ~25% by building a RAG system to crawl, scrape, vectorize, and index site data for query answering and code generation."
    )
    projects.add_project(
        "Reinforcement Learning Stacking Bot Simulation",
        "Python",
        "Pandas",
        "Matplotlib",
        "05/2024",
        "06/2024",
        "Programmed, trained, and optimized a bot with value iteration to retrieve and stack boxes by weight optimally performing action selection and task completion with a 100% success rate."
    )
    projects.add_project(
        "Tarpaulin",
        "JavaScript",
        "Docker",
        "MySQL",
        "05/2024",
        "06/2024",
        "Created a course management RESTful API and added unit tests, CRUD operations, authentication, role-based access, and file storage for attachments."
    )
    projects.add_project(
        "AI Discord Chatbot",
        "Python",
        "JavaScript",
        "Google Cloud",
        "02/2023",
        "06/2023",
        "Designed and programmed a chatbot utilizing OpenAI's language models for users to interact with via text and voice while managing instantaneous conversations with different users."
    )
    projects.add_project(
        "Unreal Engine 4 Multiplayer FPS Game",
        "UI/UX",
        "Project Management",
        "Design",
        "09/2022",
        "06/2023",
        "In collaboration with three others, led game design decisions and created maps for a multiplayer FPS game in Unreal Engine 4 presented at OSU’s Engineering Expo."
    )
    projects.add_project(
        "MLVI System POC",
        "C#",
        "Python",
        "Cognex",
        "05/2022",
        "09/2022",
        "Collected data, developed, trained, and tested a machine learning visual inspection defect detection system. System proved 20% more consistent in detection accuracy than engineers."
    )
    projects.add_project(
        "Small Shell",
        "C",
        "Assembly",
        "VIM",
        "02/2022",
        "03/2022",
        "Built a lightweight custom shell supporting command execution, I/O redirection, background processes, and signal handling similar to Windows command prompt."
    )
    projects.add_project(
        "Stats.gg",
        "Express",
        "HTML",
        "CSS",
        "05/2021",
        "06/2021",
        "Collaborated with a small team to design and develop desktop and mobile friendly frontend web pages for an esports stat tracking platform. Integrated dynamic content and cookies."
    )
    projects.add_project(
        "A Circles Game",
        "C#",
        "UI/UX",
        "Object Oriented",
        "09/2018",
        "06/2019",
        "Made a mobile game in the Unity engine published and monetized with ads on the Google Play Store and App Store for Android and iOS in collaboration with a colleague."
    )
    
    experience.add_experience(
        "Ka Tech",
        "Co-Founder & Backend Developer",
        "Remote",
        "06/2024",
        "Present",
        "Co-founded a startup serving small businesses custom websites and software, acquiring initial clients within 2 months of launch for custom sites and web apps.",
        "Led an agile cross-functional team of 10 developers to deliver features and bug fixes.",
        "Scaled company MMR by $650+ within 5 months of deploying RealDoc, a subscription based web app."
    )

    experience.add_experience(
        "Intel",
        "BIOS Firmware Intern",
        "Remote",
        "06/2023",
        "12/2023",
        "Performed cross-platform integrations of Memory Reference Code on by porting features and bug fixes for an unreleased flagship product. Tested and passed +9 changes on silicon.",
        "Reduced debugging overhead in log retrieval by ~15% for firmware developers by implementing Jenkins CI features for artifact archiving and dashboard synchronization.",
        "Improved team onboarding process and firmware documentation by authoring/maintaining +20 pages for CI, MRC, debugging processes, and best known practices."
    )

    experience.add_experience(
        "Tektronix",
        "Operations Intern",
        "Beaverton, OR",
        "03/2022",
        "12/2022",
        "Created Robotic Process Automation POCs for planners and buyers to save ~60% of time spent rescheduling orders and parts trolling using UiPath.",
        "Developed a machine learning based visual inspection system 20% more consistent than human operators in detecting defects by training a neural network on manufacturing data.",
        ""
    )

    experience.add_experience(
        "Chemeketa",
        "CAPS Assistant",
        "Salem, OR",
        "07/2019",
        "03/2020",
        "Served as front desk reception for the college’s access programs office handing phone calls and performing data entry.",
        "Provided technical support to staff occasionally and unofficial CS tutoring in unique cases.",
        ""
    )
    
    skills.add_skill("Python", "Programming Languages")
    skills.add_skill("JavaScript/TypeScript", "Programming Languages")
    skills.add_skill("C#/.NET", "Programming Languages")
    skills.add_skill("C/C++", "Programming Languages")
    skills.add_skill("Java", "Programming Languages")
    skills.add_skill("SQL", "Programming Languages")
    skills.add_skill("Groovy", "Programming Languages")
    skills.add_skill("HTML/CSS", "Programming Languages")

    skills.add_skill("Flask", "Frameworks/Libraries")
    skills.add_skill("PyTorch", "Frameworks/Libraries")
    skills.add_skill("RAG Systems", "Frameworks/Libraries")
    skills.add_skill("Model Context Protocol (MCP)", "Frameworks/Libraries")
    skills.add_skill("Vector Databases", "Frameworks/Libraries")
    skills.add_skill("Express", "Frameworks/Libraries")
    skills.add_skill("Docker", "Frameworks/Libraries")
    skills.add_skill("Langchain", "Frameworks/Libraries")
    skills.add_skill("Word2vec", "Frameworks/Libraries")
    skills.add_skill("MPI", "Frameworks/Libraries")
    skills.add_skill("OpenMP", "Frameworks/Libraries")
    skills.add_skill("SIMD SSE", "Frameworks/Libraries")
    skills.add_skill("CUDA", "Frameworks/Libraries")
    skills.add_skill("OpenCL", "Frameworks/Libraries")

    skills.add_skill("Node.js", "Platforms/Tools")
    skills.add_skill("RESTful APIs", "Platforms/Tools")
    skills.add_skill("AWS", "Platforms/Tools")
    skills.add_skill("Jenkins CI", "Platforms/Tools")
    skills.add_skill("Playwright", "Platforms/Tools")
    skills.add_skill("Jupyter", "Platforms/Tools")
    skills.add_skill("Wandb", "Platforms/Tools")
    skills.add_skill("MongoDB", "Platforms/Tools")
    skills.add_skill("MySQL", "Platforms/Tools")
    skills.add_skill("UiPath", "Platforms/Tools")
    skills.add_skill("Power Automate", "Platforms/Tools")
    skills.add_skill("Postman", "Platforms/Tools")
    skills.add_skill("Wireshark", "Platforms/Tools")
    skills.add_skill("Visual Studio", "Platforms/Tools")
    skills.add_skill("Cognex", "Platforms/Tools")
    skills.add_skill("Oracle EBS", "Platforms/Tools")
    skills.add_skill("Pinecone", "Platforms/Tools")
    skills.add_skill("RPA", "Platforms/Tools")
    skills.add_skill("Web Applications", "Platforms/Tools")
    skills.add_skill("VIM", "Platforms/Tools")
    skills.add_skill("PythonSV", "Platforms/Tools")

    skills.add_skill("Agile/Waterfall", "Other")
    skills.add_skill("Solution Architecture", "Other")
    skills.add_skill("Unit Testing", "Other")
    skills.add_skill("Project Management", "Other")
    skills.add_skill("Issue Spotting", "Other")
    skills.add_skill("UI/UX", "Other")
    skills.add_skill("ERD Design", "Other")
    skills.add_skill("Object-Oriented", "Other")
    skills.add_skill("PC Hardware", "Other")
    skills.add_skill("Leadership", "Other")
    skills.add_skill("Debugging", "Other")
    skills.add_skill("Prompt Engineering", "Other")
    skills.add_skill("Text Processing", "Other")
    skills.add_skill("Automations", "Other")
    skills.add_skill("Memory Reference Code (MRC)", "Other")
    skills.add_skill("Shell Scripting", "Other")

if __name__ == "__main__":
    main()