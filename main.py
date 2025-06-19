from modules.window import MainWindow
from pygame.locals import NOFRAME, DOUBLEBUF
from modules.config import load_config, save_config
import sys
import platform


def main_body() -> None:
    config = load_config()

    title = "Minecraft clock widget"
    flags = NOFRAME | DOUBLEBUF
    fps = config.fps
    debug = config.debug

    main_window = MainWindow(title, flags, fps, config)
    main_window.start_loop(debug)

    save_config(config)

    return 0


if __name__ == "__main__":
    if platform.system() == "Windows" and int(platform.version().split(".")[0]) > 6:
        sys.exit(main_body())

    else:
        raise EnvironmentError("App works with windows 10 and newer only. Sorry :(")
