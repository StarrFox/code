"""
small utility to compare the simularity and difference between two dirs
"""

from pathlib import Path
from sys import argv



def main():
    dir1 = Path(argv[1])
    dir2 = Path(argv[2])

    if not dir1.exists():
        exit("dir1 doesnt exsist")

    if not dir2.exists():
        exit("dir2 doesnt exsist")

    if argv[2] == "--onlydiff":
        onlydiff = True
    else:
        onlydiff = False

    dir1_files = list(dir1.iterdir())
    dir2_files = list(dir2.iterdir())

    same = []
    diff = []


    for file in dir1_files:
        if file in dir2_files:
            same.append(file.name)
        else:
            diff.append(f"{file.name} from {dir1.name}")

    for file in dir2_files:
        if file not in dir1_files:
            diff.append(f"{file.name} from {dir2.name}")

    if not onlydiff:
        print("Simularities:\n\t" + "\n\t".join(same))

    print("Differencies:\n\t" + "\n\t".join(diff))


if __name__ == "__main__":
    main()
