import os, logging, pprint
from openai import OpenAI, APIConnectionError
import util
from log import logger, log_function

class Generator:
    def __init__(self, skillmap_dir:str, prompt_dir:str, generation_dir:str):
        self.TOP_LEVEL_NAME = "unit"
        self.INFO_FILE = "course-info.yaml"
        self.skillmap_dir = skillmap_dir
        self.prompt_dir = prompt_dir
        self.generation_dir = generation_dir
        self.course = self.parse_course()

    @log_function(log_level=logging.DEBUG)
    def get_unit_paths(self, path:str) -> list[str]:
        paths = [os.path.join(path, name) for name in sorted(os.listdir(path)) if name.lower().startswith(self.TOP_LEVEL_NAME)]
        file_paths = [path for path in paths if os.path.isfile(path)]
        return file_paths

    @log_function(log_level=logging.DEBUG)
    def parse_info(self, info_file:str) -> tuple[str,str]:
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
        info = self.parse_info(self.INFO_FILE)
        course['title'] = info['title']
        course['description'] = info['description']
        course['units'] = self.parse_skillmap(self.skillmap_dir)
        return course

    def substitute(self, text:str, substitutions:dict[str,str]) -> str:
        for word, sub in substitutions.items():
            text = text.replace(word, sub)
        return text

    def get_prompt(self, file_name:str, substitutions:dict[str,str]) -> str:
        prompt_path = os.path.join(self.prompt_dir, file_name)
        prompt = util.read_file(prompt_path)
        return self.substitute(prompt, substitutions)

    def get_page_description(self, page:object) -> str:
        description = f"objective: \"{page['objective']}\""
        description += "\nskills:"
        for skill in page['skills']:
            description += f"\n- skill: \"{skill}\""
        return description

    def create_message(self, role: str,
                    message: str) -> dict[str,str]:
        return { "role": role, "content": message }

    def parse_response_content(self, chat_completion) -> str:
        return chat_completion.choices[0].message.content

    @log_function(log_level=logging.DEBUG)
    def fetch_gpt_response(self, prompt:str,
                           messages:list[dict[str,str]],
                           model:str="gpt-3.5-turbo",
                           timeout:int=120) -> tuple[list[dict[str,str]],str]:
        client = OpenAI(
            api_key = util.get_openai_key(),
            timeout = timeout
        )

        response = ""
        messages.append(self.create_message("user", prompt))
        try:
            chat_completion = client.chat.completions.create(
                model = model,
                messages = messages,
            )    
            response = self.parse_response_content(chat_completion)
            messages.append(self.create_message("assistant", response))
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

    def get_setup_messages(self, path:str) -> list[dict[str,str]]:
        context = os.path.join(path, "context.md")
        format = os.path.join(path, "format.md")
        setup = {
            "system": util.read_file(context),
            "user": util.read_file(format),
        }
        return [self.create_message(role, text) for role, text in setup.items()]
        
    @log_function(log_level=logging.DEBUG)
    def generate_page(self, prompt_file:str, substitutions:dict[str,str]) -> None:
        prompt = self.get_prompt(prompt_file, substitutions)
        messages = self.get_setup_messages(self.prompt_dir)
        messages.append(self.create_message("user", prompt))

        logger.info(f"Sending prompt:\n{pprint.pformat(messages)}")

        # generated_page = f"MY GENERATED PAGE at {util.get_time()}\n" # Dummy for avoiding using Chat GPT API
        messages, generated_page = self.fetch_gpt_response(prompt, messages)
        return generated_page

