import os, logging
import util
from log import logger, log_debug, log_info

SKILLMAP_DIR_PATH = "skillmaps/dd1396/skillmap"
GENERATED_DIR_PATH = "responses/test"
PROMPT_FILE_PATH = "prompts/new_prompt/new_prompt.md"
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

def get_prompt(path:str, page:object) -> str:
    # TODO: maybe read substitutions from a file, with som sensible default
    substitutions = {
        "NUM_QUESTIONS": "10",
        "QUESTION_TYPE": "MCQ",
        "PAGE_INFO": str(page),
    }
    prompt = util.read_file(path)
    return substitute(prompt, substitutions)

def get_test_page_description(course:object) -> object:
    return course['units'][0]['content'][0]['content'][0] # Get first page in first module

# FIXME: add these paths as parameters instead
skillmap_dir_path = util.get_subpath(SKILLMAP_DIR_PATH)
generated_dir_path = util.get_subpath(GENERATED_DIR_PATH)
prompt_path = util.get_subpath(PROMPT_FILE_PATH)

course = parse_course(skillmap_dir_path)
test_page_description = get_test_page_description(course)
prompt = get_prompt(prompt_path, test_page_description)

# print(f"prompt={prompt}")

@log_info
@log_debug
def generate_page(path:str, prompt:str) -> None:
    generated_page = "MY GENERATED PAGE\n" # fetch_gpt_response(prompt)
    util.write_file(page_path, generated_page)

page_path = os.path.join(generated_dir_path, "unit-1", "page-1.yaml")
generate_page(page_path, prompt)