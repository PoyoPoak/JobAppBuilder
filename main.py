from util import coverletter, resume, skills, experience, projects, llm, jobs
from config import Config

def main():
    print("Running...")
    # job_description = "Full Stack Developer, AI Palo Alto, CA · 1 month ago · Over 100 applicants Promoted by hirer · Actively reviewing applicants On-site Matches your job preferences, workplace type is On-site. Full-time Matches your job preferences, job type is Full-time. Easy Apply Save Save Full Stack Developer, AI at Fastino Full Stack Developer, AI Fastino · Palo Alto, CA (On-site) Easy Apply Save Save Full Stack Developer, AI at Fastino Show more options Your AI-powered job assessment Am I a good fit? Tailor my resume How can I best position myself? About the job Introduction: Are you ready to redefine the possibilities of AI? Join us at Fastino as we build the next generation of LLMs. Our team, boasting alumni from Google Research, Apple, Stanford, and Cambridge is on a mission to develop specialized, efficient AI. Fastino has raised almost $25M through our seed round and is backed by leading investors including Microsoft, Khosla Ventures, Insight Partners, NEA, CRV, Valor, Github CEO Thomas Dohmke, previous Docker CEO Scott Johnston, and others. Key Responsibilities: Design and develop interactive, scalable web applications using JavaScript, primarily Next.js and Node.js. Build and maintain server-side APIs and integrate them with front-end applications. Write, test, and deploy machine learning scripts in Python, focusing on models that can drive real-time or batch processing requirements. Work closely with data scientists to transform ML models into production-ready scripts, optimizing for performance and scalability. Conduct data analysis and preprocessing to ensure model reliability and accuracy. Architect, deploy, and maintain production-level infrastructure in cloud environments (AWS, GCP, or Azure) to support both web applications and ML operations. Ensure high availability, scalability, and security for deployed applications and services in enterprise environments. Adhere to industry best practices in code quality, testing, and documentation. Requirements: Proficiency in JavaScript, with a strong grasp of Next.js, React, and Node.js frameworks. Demonstrable experience in deploying and managing cloud infrastructure on platforms like AWS, GCP, or Azure. Knowledge of containerization (Docker, Kubernetes) and orchestration for deploying scalable applications. Preferred: Experience with data engineering practices, especially for large-scale data processing. Professional Experience: 3+ years of experience in full-stack development, ideally with a focus on JavaScript frameworks. 2+ years of experience in writing and deploying machine learning scripts in Python. Why Join Us? Supportive Environment: Benefit from the resources of Microsoft and venture funding, collaborating with top-tier talent from renowned universities. Top-Tier Compute: Enjoy a dedicated GPU cluster for research. Impactful Work: Your contributions will directly shape the future of AI applications, making technology more accessible, eco-friendly and dev friendly! Competitive Benefits: Receive competitive salary, stock options, health benefits, and more."
    
    bot = llm.ChatLLM()
    
    bot.chat(
        system_prompt=f"You are a my personal assistant who helps me with job applications. \
            You have experience as a professional software engineer hiring manager. \
            If you don't know the answer, say 'I don't know', do not make up answers. \
            You're outputting to a terminal, so format your responses accordingly. \
            "
    )
    
    
if __name__ == "__main__":
    main()