import os
import util

COURSE_INFO_FILE_NAME = "course-info.yaml"

def get_unit_paths(path:str) -> list[str]:
    paths = [os.path.join(path, name) for name in sorted(os.listdir(path)) if name.lower().startswith("unit")]
    file_paths = [path for path in paths if os.path.isfile(path)]
    return file_paths

def parse_info(skillmap_dir_path:str) -> tuple[str,str]:
    info_path = os.path.join(skillmap_dir_path, COURSE_INFO_FILE_NAME)
    return util.parse_yaml(info_path)

def parse_skillmap(skillmap_dir_path:str) -> object:
    skillmap = []
    for path in get_unit_paths(skillmap_dir_path):
        print(f"Parsing YAML: {path}")
        skillmap.append(util.parse_yaml(path))
    return skillmap

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

def get_test_page(course:object) -> object:
    return course['units'][0]['content'][0]['content'][0] # Get first page in first module

# FIXME: add these paths as parameters instead
skillmap_dir_path = util.get_subpath("skillmaps/dd1396/skillmap")
prompt_path = util.get_subpath("prompts/new_prompt/new_prompt.md")
generated_dir = util.get_subpath("responses/test")

course = parse_course(skillmap_dir_path)
test_page = get_test_page(course)
prompt = get_prompt(prompt_path, test_page)

print(f"prompt={prompt}")

# Generate 1 question
