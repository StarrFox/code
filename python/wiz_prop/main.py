import struct
import zlib
from io import BytesIO
from enum import IntFlag

from typed_bytes import TypedBytes

"""
    "class TemplateManifest": {
        "bases": [
            "PropertyClass"
        ],
        "hash": 171021254,
        "properties": {
            "m_serializedTemplates": {
                "type": "class TemplateLocation",
                "id": 0,
                "offset": 72,
                "flags": 7,
                "container": "Vector",
                "dynamic": true,
                "singleton": false,
                "pointer": false,
                "hash": 1656531664
            }
        }
    },
"""

"""
    "class TemplateLocation": {
        "bases": [
            "PropertyClass"
        ],
        "hash": 1128060484,
        "properties": {
            "m_filename": {
                "type": "std::string",
                "id": 0,
                "offset": 72,
                "flags": 7,
                "container": "Static",
                "dynamic": false,
                "singleton": false,
                "pointer": false,
                "hash": 3117322428
            },
            "m_id": {
                "type": "unsigned int",
                "id": 1,
                "offset": 104,
                "flags": 7,
                "container": "Static",
                "dynamic": false,
                "singleton": false,
                "pointer": false,
                "hash": 2301988666
            }
        }
    },
"""


class PropertyFlags(IntFlag):
    reuse_flags = 0b1
    compact_length = 0b10
    string_enums = 0b100
    compressed = 0b1000
    dirty = 0b10000


def deserialize_bind(data: TypedBytes):
    magic_header = data.buffer.read(4)
    assert magic_header == b"BINd"

    flags = PropertyFlags(data.read_typed("u4"))
    print(flags)

    is_compressed: bool = data.read_typed("bool")
    assert is_compressed is True

    size: int = data.read_typed("u4")
    assert size == 7679862

    decompressed = zlib.decompress(data.buffer.read())
    typed_decompressed = TypedBytes(BytesIO(decompressed))

    deserialize_object(typed_decompressed, flags)


def deserialize_object(data: TypedBytes, flags: PropertyFlags):
    class_hash: int = data.read_typed("u4")
    print(f"{class_hash=}")
    assert class_hash in (171021254, 1128060484)

    class_size: int = data.read_typed("u4")
    print(f"{class_size=}")

    match class_hash:
        case 171021254:
            print("TemplateManifest")
            templates = deserialize_property(data, flags)


def deserialize_property(data: TypedBytes, flags: PropertyFlags):
    property_size: int = data.read_typed("u4")

    property_hash: int = data.read_typed("u4")
    assert property_hash in (1656531664, 3117322428, 2301988666)

    match property_hash:
        case 1656531664:
            print("property TemplateLocation")
            vector_length = data.read_typed("u4")
            while data.buffer.tell() < 



if __name__ == "__main__":
    with open("game_data/TemplateManifest.xml", "rb") as fp:
        data = fp.read()
    
    typed_data = TypedBytes(BytesIO(data))

    deserialize_bind(typed_data)




# stream = open("game_data/TemplateManifest.xml", "rb").read()

# position = 0

# # this is hash
# type_tag = struct.unpack("<I", stream[position:4])[0]

# assert type_tag == 171021254

# position += 4

# while len(stream) > position:
#     # this is hash
#     property_tag = struct.unpack("<I", stream[position:4])[0]

#     assert property_tag == 1656531664



