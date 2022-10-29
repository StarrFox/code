use std::io;
use std::io::Write;

use nom::{
    branch::alt,
    character::complete::{char as parse_char, u32 as parse_u32},
    combinator::value,
    sequence::tuple,
    IResult,
};

#[derive(Clone)]
enum Operator {
    Add,
    Sub,
}

struct Expression {
    operand1: u32,
    operator: Operator,
    operand2: u32,
}

fn parse_operator(input: &str) -> IResult<&str, Operator> {
    alt((
        value(Operator::Add, parse_char('+')),
        value(Operator::Sub, parse_char('-')),
    ))(input)
}

fn parse_expression(input: &str) -> IResult<&str, Expression> {
    let (input, (operand1, operator, operand2)) =
        tuple((parse_u32, parse_operator, parse_u32))(input)?;
    Ok((
        input,
        Expression {
            operand1,
            operator,
            operand2,
        },
    ))
}

fn main() -> Result<(), std::io::Error> {
    let mut input_buffer = String::new();

    loop {
        print!(">> ");
        io::stdout().flush()?;
        io::stdin().read_line(&mut input_buffer)?;

        let to_parse = input_buffer.replace(" ", "");

        match parse_expression(&to_parse) {
            Ok((_, expression)) => {
                let result = match expression.operator {
                    Operator::Add => expression.operand1 + expression.operand2,
                    Operator::Sub => expression.operand1 - expression.operand2,
                };

                println!("result was {result}");
            }

            Err(_) => {
                println!("Invalid input");
            }
        }

        input_buffer.clear();
    }
}
