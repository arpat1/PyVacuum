import argparse
import os
import platform
import re
import subprocess
import threading
from bs4 import BeautifulSoup
from dotenv import load_dotenv


if not os.path.exists("bueeld.config.env"):
    raise FileNotFoundError("bueeld.config.env not finded")

load_dotenv(dotenv_path="bueeld.config.env")

config = {
    "PATH_TO_DEV_HTML": os.getenv("PATH_TO_DEV_HTML"),
    "PATH_TO_PROD_HTML": os.getenv("PATH_TO_PROD_HTML"),
    "PATH_TO_APP": os.getenv("PATH_TO_APP"),
    "PATH_TO_APP_ENV": os.getenv("PATH_TO_APP_ENV"),
    "#CORE_PORT": [os.getenv("CORE_PORT"), 8000],
    "#VIEW_PORT": [os.getenv("VIEW_PORT"), 5173],
    "#PM": [os.getenv("PM"), "pnpm"],
    "#RUN_DEV_COMMAND": [os.getenv("RUN_DEV_COMMAND"), "run dev"],
    "#RUN_BUILD_COMMAND": [os.getenv("RUN_BUILD_COMMAND"), "run build"],
}

def unpack_unrequired_kv(key: str):
    clear_key = key.split("#")[1]
    value = config[key]
    if type(value) is list and value[1]:
        del config[key]
        config[clear_key] = value[0] if value[0] else value[1]
    else:
        raise ValueError(f"Empty default value for unrequired key: {key}")

for key, value in config.copy().items():
    if not value:
        raise ValueError(f"Empty value for {key}")
    
    if key.startswith("#"):
        unpack_unrequired_kv(key)

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

app_exist = os.path.exists(config["PATH_TO_APP"]) and os.path.exists(config["PATH_TO_APP_ENV"])

if not app_exist:
    if not os.path.exists(config["PATH_TO_APP"]):
        raise FileNotFoundError("Incorrect path for PATH_TO_APP!")
    raise FileNotFoundError("Incorrect path for PATH_TO_APP_ENV!")

parser = argparse.ArgumentParser(description="Preparing files and run eel app")

subparser = parser.add_subparsers(dest="command")

parser_run = subparser.add_parser("run", help="run the app")
parser_run.add_argument("option", choices=["dev", "build"], help="dev - running app by using dev sources, build - running app by using build res")

args = parser.parse_args()

if args.command == "run":
    with open(config["PATH_TO_DEV_HTML"], encoding="utf-8") as file:
        soup = BeautifulSoup(file, "lxml")

        localhost_eel = f"http://localhost:{config['CORE_PORT']}/eel.js"
        static_eel = "/eel.js"
        arg_url_kv = {
            "dev": localhost_eel,
            "build": static_eel
        }

        script = soup.find("script", src=re.compile(".*/eel.js$"))

        script_line_index: int
        head_close_line_index: int

        lines: list

        with open(config["PATH_TO_DEV_HTML"], encoding="utf-8") as file:
            lines = file.readlines()
            for index, line in enumerate(lines):
                if script:
                    if "/eel.js" in line:
                        script_line_index = index
                        # print(index)
                if "</head>" in line:
                    head_close_line_index = index
                    # print(index)
        
        spaces_count = 0
        for s in lines[head_close_line_index-2]:
            if s == " ":
                spaces_count += 1
                continue
            break

        if script:
            src = script["src"]
            if src == static_eel or src == localhost_eel:
                if args.option in arg_url_kv:
                    url_type_arg = {v:k for k, v in arg_url_kv.items()}[src]

                    if url_type_arg != args.option:
                        script["src"] = arg_url_kv[args.option]
                        lines[script_line_index] = " " * spaces_count + str(script) + "\n"

                        print(spaces_count)

                        with open(config["PATH_TO_DEV_HTML"], mode="w", encoding="utf-8") as file:
                            file.writelines(lines)
        else:
            eel_script = soup.new_tag("script", src=arg_url_kv[args.option], defer="")
            str_eel_script = " " * spaces_count + str(eel_script) + "\n"

            lines.insert(head_close_line_index, str(str_eel_script))

            with open(config["PATH_TO_DEV_HTML"], mode="w", encoding="utf-8") as file:
                file.writelines(lines)

    def run_command(command):
        subprocess.run(
            command,
            shell=True,
            check=True,
        )


    def get_command(app_side: str):
        os = platform.system()
        if app_side == "view":
            mode_command_kv = {
                "dev": config["RUN_DEV_COMMAND"],
                "build": config["RUN_BUILD_COMMAND"]
            }
            mode = args.option
            path_except_html = config["PATH_TO_DEV_HTML"].split("/")[:-1]
            SRC_FOLDER_PATH = "/".join(path_except_html)

            return f"cd {SRC_FOLDER_PATH} && {config["PM"]} {mode_command_kv[mode]}"
        elif app_side == "core":
            os_interpreter_kv = {
                "Windows": f"{config['PATH_TO_APP_ENV']}/Scripts/python.exe",
                "Linux": f".{config["PATH_TO_APP_ENV"]}/bin/python",
            }

            os_interpreter_kv["Darwin"] = os_interpreter_kv["Linux"]

            return f"\"{os_interpreter_kv[os]}\" {config['PATH_TO_APP']}"
    
    if args.option == "build":
        run_command(get_command("view"))
        run_command(get_command("core"))
    elif args.option == "dev":
        run_command(get_command("core"))
        run_command(get_command("view"))