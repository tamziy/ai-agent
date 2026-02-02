import argparse
import sys
from google.genai import types
from llm import call_llm

def main():
    print("Hello from ai-agent!")

    parser = argparse.ArgumentParser(description="Gemini LLM")
    parser.add_argument("user_prompt", type=str, help="Enter a prompt for the agent")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    for _ in range(30):
        response = call_llm(messages, args)
        
        if response.function_calls is None:
            print(response.text)
            break

        if _ == 29:
            print("Limit reached")
            sys.exit(1)




            




if __name__ == "__main__":
    main()
