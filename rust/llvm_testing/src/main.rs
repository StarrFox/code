use chumsky::prelude::*;
use inkwell::{
    builder::Builder,
    context::Context,
    execution_engine::{ExecutionEngine, JitFunction},
    module::Module,
};

#[derive(Clone)]
enum Instr {
    Left,
    Right,
    Incr,
    Decr,
    Read,
    Write,
    Loop(Vec<Self>),
}

fn parser() -> impl Parser<char, Vec<Instr>, Error = Simple<char>> {
    recursive(|bf| {
        choice((
            just('<').to(Instr::Left),
            just('>').to(Instr::Right),
            just('+').to(Instr::Incr),
            just('-').to(Instr::Decr),
            just(',').to(Instr::Read),
            just('.').to(Instr::Write),
            bf.delimited_by(just('['), just(']')).map(Instr::Loop),
        ))
        .repeated()
    })
}

type VoidFunc = unsafe extern "C" fn();

fn main() {
    let context = Context::create();
    let module = context.create_module("base");
    let builder = context.create_builder();
    let execution_engine = module
        .create_jit_execution_engine(inkwell::OptimizationLevel::None)
        .unwrap();

    let void_func = context.void_type().fn_type(&[], false);
    let main_func = module.add_function("main", void_func, None);

    let basic_block = context.append_basic_block(main_func, "main");

    builder.position_at_end(basic_block);
    builder.build_return(None);

    let amain: JitFunction<VoidFunc> = unsafe {execution_engine.get_function("main").unwrap()};

    unsafe {amain.call()};
}
