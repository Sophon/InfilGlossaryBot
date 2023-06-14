import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

TOKEN = os.getenv("DEV_TOKEN")
URL = "https://glossary.infil.net/"
GITHUB = "https://github.com/Sophon/InfilGlossaryBot"
JSON_URL = "https://glossary.infil.net/json/glossary.json"
RATE_OF_LOGGING_IN_SECONDS = 604800
GFYCAT = "https://gfycat.com"
