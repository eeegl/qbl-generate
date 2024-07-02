import util
from generator import Generator

SKILLMAP_DIR = util.get_subpath("skillmaps/dd1396/skillmap/")
PROMPT_DIR = util.get_subpath("prompts/new_prompt/")
GENERATED_DIR = util.get_subpath("responses/")

generator = Generator(SKILLMAP_DIR, PROMPT_DIR, GENERATED_DIR)
generator.generate_course()