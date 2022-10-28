
from pathlib import Path
from sys import argv


def main():
    directory = Path(input('Dir? ').strip('"'))

    lines = 0
    files = 0

    for file in directory.glob('**/*.py'):
        file_obj = file.open(encoding='utf-8')
        try:
            lines += len(
                [line for line in file_obj.readlines()
                if len(line) > 0 and not line.strip().startswith('#')]
                )
            files += 1
        except Exception as e:
            print("Couldn't read " + str(file) + ':\n' + str(e))
        file_obj.close()

    print(f'{lines=}', f'{files=}')

if __name__ == "__main__":
    main()
