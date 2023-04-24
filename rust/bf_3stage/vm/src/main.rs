use std::fs;
use std::io;
use std::io::StdoutLock;
use std::io::Write;

#[derive(Debug)]
enum Instruction {
    AdvanceCell(usize),
    DevanceCell(usize),
    IncrementData(usize),
    DecrementData(usize),
    WriteIo,
    ReadIo,
    Loop(Vec<Instruction>),
}

struct Vm {
    source: String
}

impl Vm {
    fn parse(&self) -> Vec<Instruction> {
        let mut instructions: Vec<Instruction> = Vec::new();

        let mut chain = 0;
        let mut last_char = char::default();

        let mut stacks: Vec<Vec<Instruction>> = Vec::new();

        for character in self.source.chars() {
            match character {
                '>' | '<' | '+' | '-' => {
                    if character == last_char {
                        instructions.last().unwrap()
                    }

                    if character != chain_char {
                        let instruction = match character {
                            '>' => Instruction::AdvanceCell(chain),
                            '<' => Instruction::DevanceCell(chain),
                            '+' => Instruction::IncrementData(chain),
                            '-' => Instruction::DecrementData(chain),
                            _ => unreachable!() 
                        };

                        // this pushes to instructions if there is no loop stack
                        stacks.last_mut().unwrap_or(&mut instructions).push(instruction);

                        chain = 1;
                        chain_char = character;
                    } else {
                        chain += 1;
                    }
                }
                '.' => {
                    stacks.last_mut().unwrap_or(&mut instructions).push(Instruction::WriteIo);
                }
                ',' => {
                    stacks.last_mut().unwrap_or(&mut instructions).push(Instruction::ReadIo);
                }
                '[' => stacks.push(Vec::new()),
                ']' => instructions.push(Instruction::Loop(stacks.pop().unwrap())),
                // anything else is a comment
                _ => ()
            }
        }

        instructions
    }

    fn execute_instructions(
        &self,
        instructions: Vec<Instruction>,
        cells: &mut [usize],
        cell_position: &mut usize,
        stdout: &mut StdoutLock
    ) {
        for instruction in instructions {
            match instruction {
                Instruction::AdvanceCell(amount) => *cell_position += amount,
                Instruction::DevanceCell(amount) => *cell_position -= amount,
                Instruction::IncrementData(amount) => cells[*cell_position] += amount,
                Instruction::DecrementData(amount) => cells[*cell_position] -= amount,
                Instruction::WriteIo => drop(stdout.write(&[cells[*cell_position] as u8])),
                Instruction::ReadIo => todo!("who even uses this"),
                Instruction::Loop(instructions) => self.execute_instructions(instructions, cells, cell_position, stdout)
            }
        }
    }

    pub fn execute(&self) {
        let instructions = self.parse();

        dbg!(instructions);
        return;

        let mut cells = [0; 30000];
        let mut cell_position = 0;

        let mut stdout = io::stdout().lock();

        self.execute_instructions(instructions, &mut cells, &mut cell_position, &mut stdout)
    }
}

fn main() {
    //let program = fs::read_to_string("program.bf").unwrap();

    let vm = Vm{source: "++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.".to_string()};
    vm.execute();
}
