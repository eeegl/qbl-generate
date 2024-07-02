import os, logging, pprint
from openai import OpenAI, APIConnectionError
import util
from log import logger, log_function
from skillmap_parser import SkillmapParser

class Generator:
    def __init__(self, skillmap_dir:str, prompt_dir:str, generation_dir:str):
        self.INFO_FILE = "course-info.yaml"
        self.skillmap_dir = skillmap_dir
        self.prompt_dir = prompt_dir
        self.generation_dir = generation_dir
        self.course = SkillmapParser(skillmap_dir, self.INFO_FILE).parse_course()

    def create_message(self, role:str, message:str) -> dict[str,str]:
        return { "role": role, "content": message }

    def create_setup_messages(self, path:str) -> list[dict[str,str]]:
        context = os.path.join(path, "context.md")
        format = os.path.join(path, "format.md")
        setup = {
            "system": util.read_file(context),
            "user": util.read_file(format),
        }
        return [self.create_message(role, text) for role, text in setup.items()]
        
    def get_response_content(self, chat_completion) -> str:
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
            response = self.get_response_content(chat_completion)
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

    @log_function(log_level=logging.DEBUG)
    def generate_page(self, prompt_file:str, substitutions:dict[str,str]) -> None:
        prompt_path = os.path.join(self.prompt_dir, prompt_file)
        prompt = util.get_prompt(prompt_path, substitutions)
        messages = self.create_setup_messages(self.prompt_dir)
        messages.append(self.create_message("user", prompt))

        logger.info(f"Sending prompt:\n{pprint.pformat(messages)}")

        # generated_page = f"MY GENERATED PAGE at {util.get_time()}\n" # Dummy for avoiding using Chat GPT API
        messages, generated_page = self.fetch_gpt_response(prompt, messages)

        logger.info(f"Received response:\n{generated_page}")
        return generated_page

