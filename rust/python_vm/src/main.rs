use std::io::Cursor;

use byteorder::ReadBytesExt;

struct Instruction {
    opcode: u16,
    argument: u16,
}

impl Instruction {
    pub fn from_bytes(bytes: &mut Cursor<&[u8]>) -> Self {
        let opcode = bytes.read_u8().unwrap();
        let argument = bytes.read_u8().unwrap();
        Instruction {
            opcode: opcode as u16,
            argument: argument as u16,
        }
    }
}

struct Disassembler {
}

impl Disassembler {
    pub fn disassemble(self) -> Vec<Instruction>{
        todo!()
    }
}

fn main() {
    println!("Hello, world!");
}
