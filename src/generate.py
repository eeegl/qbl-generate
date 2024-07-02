import os
import util
from generator import Generator

SKILLMAP_DIR = util.get_subpath("skillmaps/dd1396/skillmap/")
PROMPT_DIR = util.get_subpath("prompts/new_prompt/")
GENERATED_DIR = util.get_subpath("responses/test/")

generator = Generator(SKILLMAP_DIR, PROMPT_DIR, GENERATED_DIR)

for unit in generator.course['units']:
    title = unit['title']
    content = unit['content']
    content_path = os.path.join(GENERATED_DIR, title)
    os.makedirs(content_path, exist_ok=True)
    generator.generate_contents(content_path, content)

# page_description = util.get_page_description(generator.course['units'][0]['content'][0]['content'][1])
# page_file_path = os.path.join(generator.generation_dir, "unit-1", "page-1.yaml")

# prompt_subs = {
#     "NUM_QUESTIONS": "10",
#     "QUESTION_TYPE": "MCQ",
#     "DESCRIPTION": str(page_description),
# }
# page = generator.generate_page("prompt.md", prompt_subs)

# improvement_subs = {
#     "PAGE": page,
# }

# improved_page = generator.generate_page("improvement.md", improvement_subs)
# util.write_file(page_file_path, f"# ---------- NEW PAGE (at {util.get_time()})\n\n")
# util.write_file(page_file_path, improved_page)
# util.write_file(page_file_path, "\n\n")