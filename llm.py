import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from call_function import available_functions, call_function
from config import SYSTEM_PROMPT

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def call_llm(messages, args):
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

    candidates = response.candidates
    for candidate in candidates:
        messages.append(candidate.content)
    
    function_results = []
    if response.function_calls:
        for call in response.function_calls:
            function_call_result = call_function(call, args.verbose)

            if not function_call_result.parts:
                raise Exception("types.Content.parts is empty")

            if function_call_result.parts[0] is None:
                raise Exception("FunctionResponse object is None")
            
            function_results.append(function_call_result.parts[0])

            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
    messages.append(types.Content(role="user", parts=function_results))
    return response