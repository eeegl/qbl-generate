import os, logging, pprint
from openai import OpenAI, APIConnectionError
import util
from log import logger, log_debug, log_info

SKILLMAP_DIR_PATH = "skillmaps/dd1396/skillmap/"
GENERATED_DIR_PATH = "responses/test/"
PROMPT_DIR_PATH = "prompts/new_prompt/"
# PROMPT_FILE_PATH = "prompts/new_prompt/new_prompt.md"
COURSE_INFO_FILE_NAME = "course-info.yaml"

@log_debug
def get_unit_paths(path:str) -> list[str]:
    paths = [os.path.join(path, name) for name in sorted(os.listdir(path)) if name.lower().startswith("unit")]
    file_paths = [path for path in paths if os.path.isfile(path)]
    return file_paths

@log_debug
def parse_info(skillmap_dir_path:str) -> tuple[str,str]:
    info_path = os.path.join(skillmap_dir_path, COURSE_INFO_FILE_NAME)
    info = util.parse_yaml(info_path)
    return info

@log_info
@log_debug
def parse_skillmap(skillmap_dir_path:str) -> object:
    skillmap = []
    for path in get_unit_paths(skillmap_dir_path):
        logger.debug(f"Parsing YAML: {path}")
        skillmap.append(util.parse_yaml(path))
    return skillmap

@log_info
@log_debug
def parse_course(skillmap_dir_path:str) -> object:
    course = {}
    info = parse_info(skillmap_dir_path)
    course['title'] = info['title']
    course['description'] = info['description']
    course['units'] = parse_skillmap(skillmap_dir_path)
    return course

def substitute(text:str, substitutions:dict[str,str]) -> str:
    for word, sub in substitutions.items():
        text = text.replace(word, sub)
    return text

def get_prompt(file_name:str, substitutions:dict[str,str]) -> str:
    prompt_path = os.path.join(util.get_subpath(PROMPT_DIR_PATH), file_name)
    prompt = util.read_file(prompt_path)
    return substitute(prompt, substitutions)

def get_test_page_description(course:object) -> object:
    return course['units'][0]['content'][0]['content'][0] # Get first page in first module

def get_page_description(page:object) -> str:
    description = f"objective: \"{page['objective']}\""
    description += "\nskills:"
    for skill in page['skills']:
        description += f"\n- skill: \"{skill}\""
    return description

def create_message(role: str,
                   message: str) -> dict[str,str]:
    return { "role": role, "content": message }

def parse_response_content(chat_completion) -> str:
    """
    Exctract the message from the API response.
    """
    return chat_completion.choices[0].message.content

@log_info
@log_debug
def fetch_gpt_response(prompt:str,
                       messages:list[dict[str,str]],
                       model:str="gpt-3.5-turbo",
                       timeout:int=120) -> tuple[list[dict[str,str]],str]:
    client = OpenAI(
        api_key = util.get_openai_key(),
        timeout = timeout
    )

    response = ""
    messages.append(create_message("user", prompt))
    try:
        chat_completion = client.chat.completions.create(
            model = model,
            messages = messages,
        )    
        response = parse_response_content(chat_completion)
        messages.append(create_message("assistant", response))
    except APIConnectionError as e:
        print("The server could not be reached.")
        print(e)
        exit(1)
    except Exception as e:
        print("An unexpexted error occurred.")
        print(e)
        exit(1)
    logger.debug(f"Received GPT response: {response}")
    return messages, response

def get_setup_messages(path:str) -> list[dict[str,str]]:
    context = os.path.join(path, "context.md")
    format = os.path.join(path, "format.md")
    setup = {
        "system": util.read_file(context),
        "user": util.read_file(format),
    }
    return [create_message(role, text) for role, text in setup.items()]
    

# generated_page = f"MY GENERATED PAGE at {util.get_time()}\n"

@log_info
@log_debug
def generate_page(prompt_file:str, substitutions:dict[str,str]) -> None:
    # TODO: maybe read substitutions from a file, with som sensible default
    prompt = get_prompt(prompt_file, substitutions)
    messages = get_setup_messages(prompt_dir)
    messages.append(create_message("user", prompt))

    logger.info(f"Sending prompt:\n{pprint.pformat(messages)}")

    # generated_page = f"MY GENERATED PAGE at {util.get_time()}\n"
    messages, generated_page = fetch_gpt_response(prompt, messages)
    return generated_page

# FIXME: add these paths as parameters instead
skillmap_dir = util.get_subpath(SKILLMAP_DIR_PATH)
generated_dir = util.get_subpath(GENERATED_DIR_PATH)
prompt_dir = util.get_subpath(PROMPT_DIR_PATH)
# prompt_path = util.get_subpath(PROMPT_FILE_PATH)

course = parse_course(skillmap_dir)
# test_page_description = get_test_page_description(course)
page_description = get_page_description(course['units'][0]['content'][0]['content'][1])

page_file_path = os.path.join(generated_dir, "unit-1", "page-1.yaml")

prompt_subs = {
    "NUM_QUESTIONS": "10",
    "QUESTION_TYPE": "MCQ",
    "DESCRIPTION": str(page_description),
}
page = generate_page("prompt.md", prompt_subs)

improvement_subs = {
    "PAGE": page,
}
improved_page = generate_page("improvement.md", improvement_subs)

util.write_file(page_file_path, f"# ---------- NEW PAGE (at {util.get_time()})\n\n")
util.write_file(page_file_path, improved_page)
util.write_file(page_file_path, "\n\n")