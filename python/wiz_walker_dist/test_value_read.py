import pymem


ADDR = 0x1406595


def main():
    proc = pymem.Pymem("WizardGraphicalClient.exe")

    value = proc.read_bytes(ADDR, 20)
    print(value.hex())

if __name__ == "__main__":
    main()
