use std::fs;
use std::io;
use std::io::Write;
use std::{collections::HashMap, ops::Index};

fn create_jump_table(program: &str) -> HashMap<usize, usize> {
    let mut table: HashMap<usize, usize> = HashMap::new();
    let mut loop_starts: Vec<usize> = Vec::new();

    for (position, character) in program.chars().enumerate() {
        if character == '[' {
            loop_starts.push(position);
        } else if character == ']' {
            let start = loop_starts.pop();

            match start {
                Some(start) => {
                    let end = position;

                    table.insert(start, end);
                    table.insert(end, start);
                }
                None => panic!("Missing [")
            }
        }
    }

    table
}

fn execute(program: &str) {
    let mut tape = [0; 30000];

    let mut tape_position = 0;
    let mut program_position = 0;
    let jump_table = create_jump_table(program);

    // you have to use bytes to index
    let program_bytes = program.as_bytes();

    let mut stdout = io::stdout().lock();

    while program_position < program.len() {
        let instruction = program_bytes.index(program_position);

        match instruction {
            b'>' => tape_position += 1,
            b'<' => tape_position -= 1,
            b'+' => tape[tape_position] += 1,
            b'-' => tape[tape_position] -= 1,
            b'.' => drop(stdout.write(&[tape[tape_position]])),
            b',' => todo!("add ,"),
            b'[' => {
                if tape[tape_position] == 0 {
                    program_position = *jump_table.get(&program_position).unwrap();
                }
            },
            b']' => {
                if tape[tape_position] != 0 {
                    program_position = *jump_table.get(&program_position).unwrap();
                }
            },
            // everything else is a comment
            _ => ()
        }

        program_position += 1;
    }
}

fn main() {
    let program = fs::read_to_string("program.bf").unwrap();

    execute(program.as_str());
}
