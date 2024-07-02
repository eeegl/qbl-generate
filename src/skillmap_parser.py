import os, logging
import util
from log import logger, log_function

class SkillmapParser:
    def __init__(self, skillmap_dir:str, info_file:str):
        self.TOP_LEVEL_NAME = "unit"
        self.skillmap_dir = skillmap_dir
        self.info_file = info_file
        
    @log_function(log_level=logging.DEBUG)
    def get_unit_paths(self, path:str) -> list[str]:
        paths = [os.path.join(path, name) for name in sorted(os.listdir(path)) if name.lower().startswith(self.TOP_LEVEL_NAME)]
        file_paths = [path for path in paths if os.path.isfile(path)]
        return file_paths

    @log_function(log_level=logging.DEBUG)
    def parse_info(self, info_file:str) -> dict[str,str]:
        info_path = os.path.join(self.skillmap_dir, info_file)
        info = util.parse_yaml(info_path)
        return info

    @log_function(log_level=logging.DEBUG)
    def parse_skillmap(self, skillmap_dir:str) -> object:
        skillmap = []
        for path in self.get_unit_paths(skillmap_dir):
            logger.debug(f"Parsing YAML: {path}")
            skillmap.append(util.parse_yaml(path))
        return skillmap

    @log_function(log_level=logging.DEBUG)
    def parse_course(self) -> object:
        course = {}
        info = self.parse_info(self.info_file)
        course['title'] = info['title']
        course['description'] = info['description']
        course['units'] = self.parse_skillmap(self.skillmap_dir)
        return course

