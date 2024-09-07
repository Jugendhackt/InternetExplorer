from dotenv import load_dotenv
from os import getenv

load_dotenv()
OPENAI_API_KEY = getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set")

def main():
  print(OPENAI_API_KEY)


if __name__ == "__main__":
  main()
