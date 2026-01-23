import os
from dotenv import load_dotenv
from google import genai


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def main():
    print("Hello from ai-agent!")

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
    )
    response_metadata = response.usage_metadata

    if response_metadata is None:
        raise RuntimeError("No response, API request likely")

    print(f"Prompt tokens: {response_metadata.prompt_token_count}")
    print(f"Response tokens: {response_metadata.candidates_token_count}")
    print(response.text)




if __name__ == "__main__":
    main()
