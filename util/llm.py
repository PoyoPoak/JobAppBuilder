import json
import sys
from typing import Optional
from config import Config
from openai import OpenAI

# import util modules for function dispatch
import util.resume as resume
import util.experience as experience
import util.projects as projects
import util.skills as skills

# map function names to their implementations
FUNCTION_MAP = {
    "generate_resume": resume.generate_resume,
    "get_all_experiences": experience.get_all_experiences,
    "add_experience": experience.add_experience,
    "edit_experience": experience.edit_experience,
    "delete_experience": experience.delete_experience,
    "get_all_projects": projects.get_all_projects,
    "add_project": projects.add_project,
    "edit_project": projects.edit_project,
    "delete_project": projects.delete_project,
    "get_all_skills": skills.get_all_skills,
    "get_skills_by_category": skills.get_skills_by_category,
    "add_skill": skills.add_skill,
    "edit_skill": skills.edit_skill,
    "delete_skill": skills.delete_skill,
}

class ChatLLM:
    """
    ChatLLM handles interactive chat sessions and one-off responses using OpenAI.
    """
    def __init__(self,
                 client: Optional[OpenAI] = None,
                 standard_model: Optional[str] = None,
                 mini_model: Optional[str] = None,
                 tool_specs = None):
        self.client = client or OpenAI()
        self.standard_model = standard_model or Config.STANDARD_MODEL
        self.mini_model = mini_model or Config.MINI_MODEL
        self.tool_specs = tool_specs if tool_specs is not None else Config.TOOL_SPECS
        self.prev_id = None

    def chat(self, 
             model: Optional[str] = None,
             system_prompt: Optional[str] = None,
             temperature: Optional[float] = None):
        print("Assistant: How can I help?")
        while True:
            try:
                user_input = input("You: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nExiting chat.")
                break

            # Prepare kwargs for the API call
            model_name = model or self.standard_model
            kwargs = {
                "model": model_name,
                "instructions": system_prompt,
                "input": [{"role": "user", "content": user_input}],
                "tools": self.tool_specs,
                "previous_response_id": self.prev_id
            }
            
            # Only add temperature if not using the reasoning model
            if temperature is not None and model is not Config.REASONING_MODEL:
                kwargs["temperature"] = temperature

            # Create the response using the OpenAI client
            resp = self.client.responses.create(**kwargs)
            
            # If tool calls are present, handle them
            follow_ups = []
            for item in resp.output:
                if item.type == "function_call":
                    fname = item.name
                    args = json.loads(item.arguments)
                    func = FUNCTION_MAP.get(fname)
                    if not func:
                        result = {"error": f"Unknown function {fname}"}
                    else:
                        print(f"Calling function: {fname} with args: {args}")
                        result = func(**args)
                    follow_ups.append({
                        "type": "function_call_output",
                        "call_id": item.call_id,
                        "output": json.dumps(result)
                    })

            # If there are follow-up function calls, create a new response to return results
            if follow_ups:
                resp = self.client.responses.create(
                    model=self.mini_model,
                    input=follow_ups,
                    previous_response_id=resp.id
                )

            # Print the assistant's response
            print("Assistant:", resp.output_text.strip())
            self.prev_id = resp.id

    def complete(self,
                 prompt: str,
                 model: Optional[str] = None,
                 system_prompt: Optional[str] = None,
                 temperature: Optional[float] = None) -> str:
        """
        Complete a prompt with optional system instructions and temperature.
        """
        kwargs = {
            "model": model or self.standard_model,
            "instructions": system_prompt,
            "input": [{"role": "user", "content": prompt}],
        }
        
        # Only add temperature if not using the reasoning model
        if temperature is not None and model is not Config.REASONING_MODEL:
            kwargs["temperature"] = temperature

        resp = self.client.responses.create(**kwargs)
        return resp.output_text.strip()

if __name__ == "__main__":
    try:
        ChatLLM().chat_loop()
    except KeyboardInterrupt:
        sys.exit(0)