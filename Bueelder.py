import argparse
import os
from dotenv import load_dotenv


if not os.path.exists("bueeld.config.env"):
    raise FileNotFoundError("bueeld.config.env not finded")

load_dotenv(dotenv_path="bueeld.config.env")

config = {
    "PATH_TO_DEV_HTML": os.getenv("PATH_TO_DEV_HTML"),
    "PATH_TO_PROD_HTML": os.getenv("PATH_TO_PROD_HTML"),
    "PORT": int(os.getenv("PORT"))
}

for key, value in config.items():
    if not value:
        raise ValueError(f"Empty value for {key}")    

is_ext_html_list = [p.split(".")[-1] == "html" for p in [config["PATH_TO_DEV_HTML"], config["PATH_TO_PROD_HTML"]]]

if sum(is_ext_html_list) != 2:
    if config["PATH_TO_DEV_HTML"].split(".") != "html":
        raise FileNotFoundError("Incorrect extension for PATH_TO_DEV_HTML")
    raise FileNotFoundError("Incorrect extension for PATH_TO_PROD_HTML!")

htmls_exists = os.path.exists(config["PATH_TO_DEV_HTML"]) and os.path.exists(config["PATH_TO_PROD_HTML"])

if not htmls_exists:
    if not os.path.exists(config["PATH_TO_DEV_HTML"]):
        raise FileNotFoundError("Incorrect path for PATH_TO_DEV_HTML!")
    raise FileNotFoundError("Incorrect path for PATH_TO_PROD_HTML!")

parser = argparse.ArgumentParser(description="Preparing files and run eel app",)

subparser = parser.add_subparsers(dest="command")

parser_run = subparser.add_parser("run", help="run the app")
parser_run.add_argument("option", choices=["dev", "build"], help="dev - running app by using dev sources, build - running app by using build res")

args = parser.parse_args()

if args.command == "run":
    if args.option == "dev":
        print("Running on dev mode")
    elif args.option == "build":
        print("Running build")