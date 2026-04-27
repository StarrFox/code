import re
from pathlib import Path
from os import environ
from io import BytesIO

"""
enviorment variables:
DISCORD_INSTALL_DIR = directory of discord install (can be missing)
"""

version_pattern = re.compile(r"\d+\.\d+\.\d+")
# to get this open discord_krisp.node and search for `IsSignedByDiscord`
function_pattern = re.compile(rb"\x55\x41\x57\x41\x56\x53\x48\x81\xec\x78\x20\x00\x00\x80\x7f\x17\x00.\x03\x48")

# /home/starr/.config/discord/0.0.127/modules/discord_krisp/discord_krisp.node
def get_krisp_module(discord_install_dir: Path | None = None) -> Path:
    if discord_install_dir is None:
        config_home = environ.get("XDG_CONFIG_HOME", None)
        if config_home is None:
            raise RuntimeError("XDG_CONFIG_HOME enviorment variable not set")

        discord_install_dir = Path(config_home) / "discord"

        if not discord_install_dir.exists():
            raise RuntimeError(f"discord not found at {config_home}/discord try setting DISCORD_INSTALL_DIR")

    version_folder = get_version_folder(discord_install_dir)

    krisp_module = version_folder / "modules/discord_krisp/discord_krisp.node"

    if not krisp_module.exists():
        raise RuntimeError(f"Kirsp module not found at {krisp_module}, has discord been run once?")

    return krisp_module


def get_version_folder(discord_install_dir: Path) -> Path:
    results = [sub_file for sub_file in discord_install_dir.iterdir() if version_pattern.match(sub_file.name) is not None]

    match len(results):
        case 1:
            return results[0]
        case 0:
            raise RuntimeError(f"No version folder found under {discord_install_dir}")
        case _:
            raise RuntimeError(f"Multiple version folders found under {discord_install_dir}")


# TODO: close discord if open
def main():
    discord_install_override = environ.get("DISCORD_INSTALL_DIR", None)

    if discord_install_override is not None:
        discord_install_override = Path(discord_install_override)
        if not discord_install_override.exists():
            raise RuntimeError(f"{discord_install_override} does not exist")

    krisp_module = get_krisp_module(discord_install_override)
    data = krisp_module.read_bytes()

    potential_functions = list(function_pattern.finditer(data))

    match len(potential_functions):
        case 1:
            function_address = potential_functions[0].start()
        case 0:
            raise RuntimeError("Unable to find function pattern in module, likely needs updating")
        case _:
            raise RuntimeError("Multiple matches for function pattern, likely needs to be longer")

    data_wrapper = BytesIO(data)
    data_wrapper.seek(function_address)
    # mov rax, 1 [48 C7 C0 01 00 00 00]
    # ret [C3]
    data_wrapper.write(b"\x48\xC7\xC0\x01\x00\x00\x00\xC3")
    data_wrapper.seek(0)

    krisp_module.write_bytes(data_wrapper.getbuffer())
    print(f"Patched {krisp_module}")


if __name__ == "__main__":
    main()
