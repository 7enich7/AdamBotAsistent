import os
import winshell


def create_startup_shortcut():
    exe_path = os.path.abspath("Adamt 3.3.exe")

    startup_folder = winshell.startup()

    shortcut_path = os.path.join(startup_folder, "MyAdam.lnk")

    try:
        with winshell.shortcut(shortcut_path) as shortcut:
            shortcut.path = exe_path
            shortcut.description = "MyAdam"
            shortcut.working_directory = os.path.dirname(exe_path)

        print("Ярлык создан в папке автозагрузки.")
    except Exception as e:
        print(f"Ошибка при создании ярлыка: {e}")


if __name__ == "__main__":
    create_startup_shortcut()