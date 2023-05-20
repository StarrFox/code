from pathlib import Path

from starrlib import TypedBytes


class DataStore:
    def __init__(self, path: Path):
        self.path = path

        self.handle = open(self.path, "ab+")
        self.typed_handle = TypedBytes(self.handle)

    def _create_ds(self, collum_data: list[tuple[str, str]]):
        self.handle.write("pydb".encode())
        # version
        self.typed_handle.write_typed("u2", 1)

        # TODO: primary key info

        for name, _type in collum_data:

            name = name.encode()
            name_len = len(name)

            # size of collum data
            self.typed_handle.write_typed("u2", 2 + name_len + 2)

            self.typed_handle.write_typed("u2", len(name))

            match _type:
                case "u4":
                    self.typed_handle.write_typed("u2", 1)
                case _:
                    raise NotImplemented()
