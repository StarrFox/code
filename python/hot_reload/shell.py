import time
from pathlib import Path


SLEEPTIME = 1


def main():
    target_file = Path("test.py")
    old_content = ""

    while True:
        if (new_content := target_file.read_text()) != old_content:
            old_content = new_content
            module_code = compile(new_content, "__main__", "exec")
            exec(module_code)

        time.sleep(SLEEPTIME)


if __name__ == "__main__":
    main()
