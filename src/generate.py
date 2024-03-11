import sys
from setup import setup
from prompting import generate_questions

if __name__ == "__main__":
    config, skillmap = setup()

    try:
        generate_questions(config, skillmap)
        print("Generation done!")
    except Exception as e:
        # raise e # Uncomment for more verbose errors
        print(e)
        sys.exit(1)
