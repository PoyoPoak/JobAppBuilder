import json
import sys
from typing import Optional
from config import Config
from openai import OpenAI

from util.resume import generate_resume

# ---------- JSON-Schema tool spec ---------- #
DEFAULT_TOOL_SPECS = [
    {
        "name": "generate_resume",
        "description": "Generate a resume based on job description and candidate data.",
        "parameters": {
            "type": "object",
            "properties": {
                "job_description": {
                    "type": "string",
                    "description": "Job description text"
                },
                "skills": {
                    "type": "array",
                    "items": {"type": "object"},
                    "description": "List of skill dictionaries"
                },
                "experiences": {
                    "type": "array",
                    "items": {"type": "object"},
                    "description": "List of experience dictionaries"
                },
                "projects": {
                    "type": "array",
                    "items": {"type": "object"},
                    "description": "List of project dictionaries"
                }
            },
            "required": ["job_description", "skills", "experiences", "projects"]
        }
    }
]

class ChatLLM:
    """
    ChatLLM handles interactive chat sessions and one-off responses using OpenAI.
    """
    def __init__(self,
                 client: Optional[OpenAI] = None,
                 standard_model: Optional[str] = None,
                 mini_model: Optional[str] = None,
                 tool_specs=None):
        self.client = client or OpenAI()
        self.standard_model = standard_model or Config.STANDARD_MODEL
        self.mini_model = mini_model or Config.MINI_MODEL
        self.tool_specs = tool_specs if tool_specs is not None else DEFAULT_TOOL_SPECS
        self.prev_id = None

    def chat_loop(self, system_prompt: Optional[str] = None):
        print("Assistant: How can I help?")
        while True:
            try:
                user_input = input("You: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nExiting chat.")
                break

            resp = self.client.responses.create(
                model=self.standard_model,
                instructions=system_prompt,
                input=[{"role": "user", "content": user_input}],
                tools=self.tool_specs,
                previous_response_id=self.prev_id,
            )
            follow_ups = []
            for item in resp.output:
                if item.type == "function_call":
                    fname = item.name
                    args = json.loads(item.arguments)
                    if fname == "generate_resume":
                        from util.resume import generate_resume
                        result = generate_resume(**args)
                    else:
                        result = {"error": f"Unknown function {fname}"}
                    follow_ups.append({
                        "type": "function_call_output",
                        "call_id": item.call_id,
                        "output": json.dumps(result)
                    })

            if follow_ups:
                resp = self.client.responses.create(
                    model=self.mini_model,
                    input=follow_ups,
                    previous_response_id=resp.id
                )

            print("Assistant:", resp.output_text.strip())
            self.prev_id = resp.id

    def generate(self, prompt: str) -> str:
        """
        Generate a one-off response for the given prompt.
        """
        resp = self.client.responses.create(
            model=self.standard_model,
            input=[{"role": "user", "content": prompt}],
            tools=self.tool_specs,
        )
        follow_ups = []
        for item in resp.output:
            if item.type == "function_call":
                fname = item.name
                args = json.loads(item.arguments)
                if fname == "generate_resume":
                    from util.resume import generate_resume
                    result = generate_resume(**args)
                else:
                    result = {"error": f"Unknown function {fname}"}
                follow_ups.append({
                    "type": "function_call_output",
                    "call_id": item.call_id,
                    "output": json.dumps(result)
                })

        if follow_ups:
            resp = self.client.responses.create(
                model=self.mini_model,
                input=follow_ups,
                previous_response_id=resp.id
            )

        return resp.output_text.strip()

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
        if temperature is not None:
            kwargs["temperature"] = temperature

        resp = self.client.responses.create(**kwargs)
        return resp.output_text.strip()

if __name__ == "__main__":
    try:
        ChatLLM().chat_loop()
    except KeyboardInterrupt:
        sys.exit(0)