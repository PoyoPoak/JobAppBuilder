from util import coverletter, resume, skills, experience, projects, llm, jobs
from config import Config

def main():
    print("Running...")
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