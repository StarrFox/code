use object::{Object, ObjectSection};
use std::fs;

fn main() {
    let file_data = fs::read("example.o").unwrap();
    let obj = object::File::parse(&file_data[..]).unwrap();

    let text_section = obj.section_by_name(".text").unwrap();
    //println!("{:x?}", text_section.data().unwrap());

    let code = text_section.data().unwrap();

    let mut buffer: Vec<u8> = Vec::new();
    let mut elf_builder = object::write::elf::Writer::new(object::Endianness::Little, true, &mut buffer);
    let file_header = object::write::elf::FileHeader {
        os_abi: object::elf::ELFOSABI_LINUX,
        abi_version: 1,
        // TODO: is this supposed to be dyn
        e_type: object::elf::ET_EXEC,
        e_machine: object::elf::EM_X86_64,
        e_entry: 0x1000,
        e_flags: 0,
    };

    elf_builder.reserve_file_header();
    elf_builder.reserve_program_headers(1);

    
}
