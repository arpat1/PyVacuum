import json
import os
import eel


if __name__ == "__main__":
    STATIC_FOLDER=os.getenv("STATIC")
    VIEW_PORT=os.getenv("VIEW_PORT")
    CORE_PORT=os.getenv("CORE_PORT")

    VIEW_DICT=json.loads(os.getenv("MODE")) # {"": "index.html"} for build, {"port": VIEW_PORT} for dev
    SIZE=(500, 500)
    POSITION=None

    eel.init(STATIC_FOLDER)
    eel.start(
        VIEW_DICT,
        port=CORE_PORT,
        size=SIZE,
        position=POSITION,
        disable_cache=True,
        cmdline_args=[
            "--new-window",
            '--user-data-dir=C:/eel_chrome_profile'
        ]
    )