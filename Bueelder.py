import os
from dotenv import load_dotenv


load_dotenv(dotenv_path="bueeld.config.env")

config = {
    "PATH_TO_DEV_HTML": os.getenv("PATH_TO_DEV_HTML"),
    "PATH_TO_PROD_HTML": os.getenv("PATH_TO_PROD_HTML"),
    "PORT": int(os.getenv("PORT"))
}

for key, value in config.items():
    if not value:
        raise ValueError(f"Empty value for {key}")