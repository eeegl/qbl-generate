import os
from openai import OpenAI, APIConnectionError
from util import read_file, write_file, write_log

def generate_questions(prompt_path : str,
                      response_path : str,
                      num_questions : int = 3) -> None:
    """
    This function does the following:
    
    1. reads a prompt from a given file,
    2. gets the response from the GPT model, and then
    3. writes the response to another given file.
    
    At the end, the received response is printed.
    """
    # Reads the prompt from the given file
    prompt = read_file(prompt_path)

    # Gets response from Chat GPT, using "gpt-3.5-turbo" by default.
    # Specify model otherwise, like the commented out code below.
    response = fetch_gpt_reply(prompt, num_questions)
    # response = fetch_gpt_reply(prompt, num_questions, "gpt-4")

    # Logs the time and which prompt file generated the questions
    description = "from " + prompt_path
    write_log(response_path, description)

    # Writes the response to the given file
    write_file(response_path, response)
    print(f"--- Wrote the following to '{response_path}':\n{response}")

def fetch_gpt_reply(prompt: str,
                    num_questions : int,
                    model: str = "gpt-3.5-turbo") -> str:
    """
    Sends the prompt and fetches the response using the Chat Completions API.

    By default, `model` is set to `gpt-3.5-turbo` as it is cheaper. 

    Set to `gpt-4` for better results.
    """
    client = OpenAI(
        api_key = get_openai_key(),
        timeout = 120 # 120 seconds, default is 10 minutes
    )

    try:
        print("--- Sending API request")
        chat_completion = client.chat.completions.create (
            messages = [
                {
                    "role": "system",
                    "content": "You are a friendly and pedagogical professor in programming,"
                               "with decades of teaching experience."
                },
                {
                    "role": "user",
                    "content": prompt + f"\n\nGenerate {num_questions} questions.",
                }
            ],
            model = model,
        )    
    except APIConnectionError as e:
        print("The server could not be reached.")
        print(e)
        exit(1)
    except Exception as e:
        print("An unexpexted error occurred.")
        print(e)
        exit(1)

    content = chat_completion.choices[0].message.content
    print("--- Request was successful")
    # print(f"Received: \n{content}") # For debugging

    return content

def get_openai_key(key_name = "OPENAI_API_KEY_KTH") -> str:
    """
    Helper function that gets the OpenAI API key saved  an environmental variable,
    by default set to `OPENAI_API_KEY_KTH`.

    NOTE: Make sure that `OPENAI_API_KEY_KTH` is set, or provide an argument
    if you have it set to another variable name.
    """
    key = os.getenv(key_name) 
    if not key:
        raise ValueError(f"Environment variable {key_name} is not set.")
    return key