import argparse
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import SYSTEM_PROMPT
from call_function import available_functions

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def main():
    print("Hello from ai-agent!")

    parser = argparse.ArgumentParser(description="Gemini LLM")
    parser.add_argument("user_prompt", type=str, help="Enter a prompt for the agent")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            tools=[available_functions]    
        )
    )
    response_metadata = response.usage_metadata

    if response_metadata is None:
        raise RuntimeError("No response, API request likely broken")
    
    if args.verbose is True:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response_metadata.prompt_token_count}")
        print(f"Response tokens: {response_metadata.candidates_token_count}")

    if response.function_calls:
        for call in response.function_calls:
            print(f"Calling function: {call.name}({call.args})")
    
    print(response.text)




if __name__ == "__main__":
    main()
