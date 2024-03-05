import os, sys
from prompting import generate_questions

if __name__ == "__main__":
    args        = sys.argv
    min_args    = 2 # Used for CLI input validation
    script_name = args[0]

    # Defaults, set as required
    num_questions = 3
    prompts_dir   = "../prompts/"   # Use "" to specify custom
    responses_dir = "../responses/" # directories from CLI

    if len(args) < min_args:
        # Validate CLI input
        raise ValueError("Too few arguments. Usage: "
                         + script_name + " <directory-path>")
    
    if len(args) > min_args: 
        # User specified number of questions, so update
        num_questions = args[2]

    # Gets directory path from CLI
    dir_path = args[1]

    # Actual question generation
    try:
        
        for file_name in os.listdir(os.path.join(prompts_dir, dir_path)):
            root, _ = os.path.splitext(file_name) # Remove file extension

            # Constructs the full paths
            prompt_path = os.path.join(prompts_dir, dir_path + root + ".in")
            response_path = os.path.join(responses_dir, dir_path + root + ".out")

            # print("prompt_path=" + prompt_path)
            # print("response_path=" + response_path)

            generate_questions(prompt_path, response_path, num_questions)
    except Exception as e:
        # raise e # Uncomment for more verbose errors
        print(e)
        sys.exit(1)
