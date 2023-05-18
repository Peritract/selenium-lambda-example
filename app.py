from os import environ as env

from dotenv import load_dotenv

def handler(event, context):
    return env.get("EXAMPLE")

if __name__ == "__main__":
    load_dotenv()
    print(handler(None, None))