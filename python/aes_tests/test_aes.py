from binascii import unhexlify

from Crypto.Cipher import AES


aes_key = bytes.fromhex("25 17 1A 2B B0 D5 03 85 C1 70 78 30 76 44 4A 54")
aes_nonce = bytes.fromhex("B8 B0 C3 52 53 C0 98 E9 78 8F BF BB B5 3F 80 0C")

# time for experiments


def hex_to_bytes(hex):
    return unhexlify(hex.replace(" ", ""))

def human_bytes(raw: bytes) -> str:
    return raw.hex(' ').upper()

test_data = [
    # Those two are fine (29 25)
    # c -> s
    hex_to_bytes("29 25 A7 8D 78 44 39 EB AE 24 CC 02 32 22 F7 8F 46 EF 4E 7C 89 7F 01 FB C7 CD 3D 80 1A 89 64 53 70 EF C3 F3 DE 34 3D DE E4 0D 5C 23 20 C5 5E E7 CE 01 1A 52 67 4B 7E 0B 41 5F E4 F9 6F 57 93 83 69 64 2F 6B F4 21 C5 B9 B3 2D 13 9D 22 68 23 B6 52 4F 92 5E 01 88 87 FA D1 75 90 C6 A5 0C A7 31 62 90 5B D8 46 85 CB 07 07 ED A5 59 40 A5 65 62 88 DC 8C 61 8A 02 F8 2E 1C F4 CC C0 B4 FA 0C 00 EC A1 B0 3F 97 8E C7 7B 09 AF E4 4E 8F 41 73 63 CB BF 95 DB 9D C6 01 48 56 9C 88 72 E9 C0 E1 E1 08 6D A7 46 D9 F7 A9 06 2B BC 6A 31 03 28 4F FD 7E 36 9A 0D 90 B8 1B 6B 52 83 71 08 63 51 54 D2 48 80 C3 C9 2B B9 91 6E CC A9 CB 13 EE 09 DD 5C 56 D2 33 85 3E 86 4A 7F 58 8D 1F 3B 32 30 35 C4 49 CC 78 CE 62 92 2E 73 24 0C 94 19 70 C9 87 82 3A 58 BB 5B A2 6F 12 BD DA 72 0F C4 4C 75 A8 EF BF 11 16 FA 60 67 0E E0 B2 BD F8 41 05 E7 4F 35 84 AF 37 43 D6 83 41 9F AD C6 0B 50 73 D4 D6 51 B9 21 0A FE 34 40 72 F5 37 23 73 D2 10 22 8B 88 F0 6D F8 7B 0E A0 7C CA 21 BF 14 87 F7 8F 2B D8 1F 62 C4 E5 3E DB 9A 7A 15 3C 86 3C 07 4D 0E 6A E6 3D 79 9C 1F 1D A7 71 CE 91 A6 99 57 63 DD DA 2E F9 44 D9 19 B5 15 EE 10 35 46 BD F1 75 A8 5A 68 29 E4 D0 F5 19 D5 20 3D D1 37 3B 5B 80 C3 55 A8 9F 73 CB AF 2F F4 1D D6 59 BC B1 CF A6 9B 59 BC 79 49 70 4F 97 F5 2C 8B F4 FE 1F 92 42 C7 F3 4A 46 7F 73 DA 6C 41 44 AA 33 AC FD 16 D8 7B 53 60 7D DD 02 14 F7 76 03 41 6F FC 6B 29 54 9B DE 4E 30 DC F8 53 9A F3 2C 26 9E A5 9E B9 C3 FB E9 89 AA 04 EC 19 C5 61 27 00 EC 57 DF 1A D6 F5 B0 60 3B 93 59 DE DD 68 F3 04 C6 FC 4A 9F 10 00 C6 B7 7C 3E 1C 9F 9A D6 12 55 88 78 7B 0F 31 2A 94 68 65 CF 76 FF 04 89 E3 91 E5 2C F9 BD 03 AC D8 74 C4 8D 06 BB 5E D8 27 88 BA 65 B2 93 2A A0 AA ED 03 F2 1E 6C 6C 0E 80 B4 22 B1 2D 05 43 24 78 48 59 13 87 0A D9 28 E9 1A 24 A9 6C 82 FC 33 6F F1 B1 88 92 84 8F 6E FF DD 31 F7 BA D0 BC 3D 01 E2 80 4D DA A2 F8 B4 13 D7 93 8D AF 2A 1C 9B 69 AC FB 10 86 18 34 24 B2 55 00 7F 35 C6 D6 23 72 1F 91 1E 79 7F 22 FC F2 54 A6 0A 56"),
    # s -> c
    hex_to_bytes("29 25 A4 8F 78 44 39 EB AE 31 C9 00 58 22 8F 0B 1E 33 F9 9C D4 0A 00 2E E9 5E 2C B3 67 CE 24 7A 0D C1 E1 C8 8C 35 37 8D 1F 27 22 11 6B 48 63 E6 08 89 2B EE A8 18 AD 2F A4 82 E7 5C CE E9 4B 6E C2 68 8E 48 5C C5 5D 9E D0 FF 84 65 4F 02 E7 2C 71 27 CD 27 14 2D 76 F1 BA 94 7D 65 A8 9C 40 A6 BE F2 FF 9E 5E 38 8A 1E 94 87 F0 22 C3 F4 84 D5 E4 0A 79 9C 7B 4C CE 93 16 F4 9B EE 85 D4 39"),
    # here it starts failing
    # c -> s
    hex_to_bytes("0C C2 EB E2 ED E2 1D C1 BE B8 63 7B 43"),
    # s -> c
    hex_to_bytes("3D 2C 9E 81 0F 86 8E B5 4B 2E 93 D1 7A B9 6F 24 0A B1 DE E7 BF"),

]


def decrypt(raw: bytes):
    aes = AES.new(aes_key, AES.MODE_GCM, nonce=aes_nonce)
    return aes.decrypt(raw)

# for data in test_data:
#     assert decrypt(data)[:2] == b"\r\xF0"

print(decrypt(test_data[0][:2]))
assert decrypt(test_data[0][:2]) == b"\r\xF0"
