import os
import re
from openai import OpenAI, APIConnectionError
from util import read_file, prepend_file, generate_log, get_time

##############################
# Question generation
##############################
def generate_questions(config : dict[str, str],
                       skillmap : dict[str, str]) -> None:
    """
    Generates the questions.

    Will generate questions for all units by default.

       - If units are given in `config`, it generates only for those units.
       - If skills are given in `config`, it generates only for those skills.
       - If both skills and units are given in `config`, skills take precedence.
    """
    prompt_path, improvement_path, responses_dir = get_paths(config)
    prompt_template = read_file(prompt_path)
    
    skills = config["skills"]
    units = config["units"]

    # Indices are used for enumerating the output files and directories.
    found_match = False
    for unit_index, unit in enumerate(skillmap["units"]):
        if not config["all"] and not skills and units and unit["name"] not in units: 
            continue
        for skill_index, skill in enumerate(unit["skills"]):
            if not config["all"] and skills and skill["name"] not in skills: 
                continue
            found_match = True

            prompt = insert_skill(prompt_template, skill["aim"])
            improvement = read_file(improvement_path)

            # API call
            print(f"--- Sending request (at {get_time()})\n" +
                  f"unit: {unit["name"]}\n" +
                  f"skill: {skill["name"]}")
            response = fetch_gpt_reply(config["gpt_model"],
                                       prompt,
                                       config["num_questions"],
                                       config["timeout"],
                                       config["improvement_enabled"],
                                       improvement)
            print(f"--- Request successful (at {get_time()})\n")

            unit_dir = format_unit_dir_name(unit["name"])
            file_name = format_skill_file_name(skill["name"])

            if config["enumeration_enabled"]:
                unit_prefix = str(unit_index + 1) + "_"
                unit_dir = unit_prefix + unit_dir
                skill_prefix = str(skill_index + 1) + "_"
                file_name = skill_prefix + file_name

            # Writes to the file
            path = os.path.join(responses_dir, unit_dir, file_name)
            prepend_file(path, response + "\n")

            # Logs metadata
            title = "Response"
            log = generate_log(title, config)
            prepend_file(path, log + "\n")
    if not found_match:
        raise ValueError("error: given units or skills not found in skillmap, " +
                         "make sure spelling and letter case is correct")

##############################
# GPT interaction
##############################
def fetch_gpt_reply(model: str,
                    prompt: str,
                    num_questions: int,
                    timeout: int,
                    improve_enabled: bool,
                    improvement_prompt: str) -> str:
    """
    Sends the prompt and fetches the response using the Chat Completions API.

    By default, `model` is set to `gpt-3.5-turbo` as it is cheaper. 

    Set to `gpt-4` for better results.
    """
    context = "You are a friendly and pedagogical professor in programming, "
    "with decades of teaching experience."
    messages = [
        create_message("system", context),
        create_message("user", prompt +
                       f"\n\nGenerate {num_questions} questions."),
    ]

    client = OpenAI(
        api_key = get_openai_key(),
        timeout = timeout
    )
    
    try:
        # print("MESSAGES:", messages)
        # API call
        response = "REGULAR DUMMY RESPONSE"
        # response = fetch_single_response(client, model, messages)

        if improve_enabled:
            print(f"--- Sending improvement request (at {get_time()})")
            messages.append(create_message("assistant", response))
            messages.append(create_message("user", improvement_prompt +
                                           "\n\nMake sure there are " +
                                          f"{num_questions} questions."))
            # print("IMPROVEMENT MESSAGES:", messages)
            # API call
            response = "IMPROVEMENT DUMMY RESPONSE"
            # response = fetch_single_response(client, model, messages)
    except APIConnectionError as e:
        print("The server could not be reached.")
        print(e)
        exit(1)
    except Exception as e:
        print("An unexpexted error occurred.")
        print(e)
        exit(1)

    # print(f"Received: \n{content}") # For debugging

    return response

##############################
# Helper functions
##############################
def insert_skill(prompt: str,
                  skill: str) -> str:
    skill_anchor = "$SKILL$"
    return prompt.replace(skill_anchor, skill)

def create_message(role: str,
                   message: str) -> str:
    return { "role": role, "content": message }

def fetch_single_response(client, model, messages):
    chat_completion = client.chat.completions.create (
        model = model,
        messages = messages,
    )    
    return get_response_content(chat_completion)

def get_response_content(chat_completion) -> str:
    """
    Exctract the content from the API response.
    """
    return chat_completion.choices[0].message.content

def format_unit_dir_name(unit: str) -> str:
    """
    Returns the given unit name with all non-alphanumeric characters converted
    to underscores. Also makes the name uppercase.
    """
    unit = unit.strip()
    unit = sanitize_special_chars(unit)
    unit_name = unit.upper()
    return unit_name

def format_skill_file_name(skill: str,
                           extension: str = ".md") -> str:
    """
    Returns the given skill name with all non-alphanumeric characters converted
    to underscores. Also makes the name lowercase.

    By default, a `.md` extension is added to the file name.
    """
    skill = skill.strip()
    skill = sanitize_special_chars(skill)
    file_name = skill.lower() + extension
    return file_name

def sanitize_special_chars(input):
    """
    Replace all repeated non-alphanumeric characters with underscores.
    """
    return re.sub(r"[^\w]+", "_", input)

def get_paths(config):
    """
    Return the prompt, improvement and responses directory paths.
    """
    root = config["root_dir"]
    prompts = config["prompts_dir"]

    prompt_path = os.path.join(root, prompts, config["prompt_file"])
    improvement_path = os.path.join(root, prompts, config["improvement_file"])
    responses_dir = os.path.join(root, config["responses_dir"])

    return [prompt_path, improvement_path, responses_dir]

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