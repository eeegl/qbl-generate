import os, yaml

def get_skillmap_dir_path() -> str:
    script_dir = os.path.abspath(__file__)
    path = os.path.abspath(os.path.join(script_dir, "../../skillmaps/dd1396/skillmap"))
    return path

def get_unit_paths(path:str) -> list[str]:
    paths = [os.path.join(path, name) for name in sorted(os.listdir(path)) if name.lower().startswith("unit")]
    file_paths = [path for path in paths if os.path.isfile(path)]
    return file_paths

def parse_yaml(path:str) -> object:
    with open(path, 'r') as file:
        parsed = yaml.safe_load(file)
    return parsed

def parse_info(skillmap_dir_path:str) -> tuple[str,str]:
    info_path = os.path.join(skillmap_dir_path, "course-info.yaml")
    return parse_yaml(info_path)

def parse_skillmap(skillmap_dir_path:str) -> object:
    skillmap = []
    for path in get_unit_paths(skillmap_dir_path):
        print(f"Parsing YAML: {path}")
        skillmap.append(parse_yaml(path))
    return skillmap

def parse_course(skillmap_dir_path:str) -> object:
    course = {}
    info = parse_info(skillmap_dir_path)
    course['title'] = info['title']
    course['description'] = info['description']
    course['units'] = parse_skillmap(skillmap_dir_path)
    return course

skillmap_dir_path = get_skillmap_dir_path()
course = parse_course(skillmap_dir_path)

for unit in course['units']:
    print(f"UNIT:\n{unit}")

