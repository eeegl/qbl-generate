import os
from openai import OpenAI, APIConnectionError
from util import read_file, write_file, write_log

def generate_questions(config : dict[str, str],
                       skillmap : dict[str, str]) -> None:
    """
    This function does the following:
    
    1. reads a prompt from a given file,
    2. gets the response from the GPT model, and then
    3. writes the response to another given file.
    
    At the end, the received response is printed.
    """
    prompt_path, response_path, num_questions = unpack_config(config)

    # Reads the prompt from the given file
    prompt_template = read_file(prompt_path)
    
    for unit in skillmap.get("units"):
        for skill in unit.get("skills"):
            prompt = replace_skill(prompt_template, skill.get("aim"))

            # Gets response from Chat GPT, using "gpt-3.5-turbo" by default.
            # Specify model otherwise, like the commented out code below.
            # response = fetch_gpt_reply(model, prompt, num_questions, timeout)
            print("-----")
            print("DUMMY FETCHED RESPONSE:") # Debug
            print(prompt) # Debug
            print("-----")

    # Logs the time and which prompt file generated the questions
    description = "from " + prompt_path
    write_log(response_path, description)

    # Writes the response to the given file
    write_file(response_path, response)
    print(f"--- Wrote the following to '{response_path}':\n{response}")

def fetch_gpt_reply(model: str,
                    prompt: str,
                    num_questions: int,
                    timeout: int) -> str:
    """
    Sends the prompt and fetches the response using the Chat Completions API.

    By default, `model` is set to `gpt-3.5-turbo` as it is cheaper. 

    Set to `gpt-4` for better results.
    """
    client = OpenAI(
        api_key = get_openai_key(),
        timeout = timeout
    )

    try:
        print("--- Sending API request")
        chat_completion = client.chat.completions.create (
            model = model,
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
        )    
    except APIConnectionError as e:
        print("The server could not be reached.")
        print(e)
        exit(1)
    except Exception as e:
        print("An unexpexted error occurred.")
        print(e)
        exit(1)

    content = get_content(chat_completion)
    print("--- Request was successful")
    # print(f"Received: \n{content}") # For debugging

    return content

def replace_skill(prompt: str,
                  skill: str) -> str:
    skill_anchor = "$SKILL$"
    return prompt.replace(skill_anchor, skill)

def get_content(chat_completion):
    return chat_completion.choices[0].message.content

def unpack_config(config):
    # Prompt path
    prompts_dir = os.path.join(config.get("root_dir"),
                                config.get("prompts_dir"))
    prompt_path = os.path.join(prompts_dir, config.get("prompt_file"))
    # Response path
    responses_dir = os.path.join(config.get("root_dir"),
                                config.get("responses_dir"))
    response_path = os.path.join(responses_dir, config.get("responses_dir"))
    # Number of questions
    num_questions = config.get("num_questions")

    return [prompt_path, response_path, num_questions]

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