import eel


if __name__ == "__main__":
    STATIC_FOLDER="src/view/dist"
    VIEW_PORT=5173
    CORE_PORT=8000

    VIEW_DICT={"": "index.html"} # {"port": VIEW_PORT} for dev
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