use pest::{Parser, iterators::Pair};

extern crate pest;
#[macro_use]
extern crate pest_derive;

#[derive(Parser)]
#[grammar = "olaf.pest"]
struct NumberParser;

fn print_pairs(pair: Pair<Rule>, depth: usize) {
    let tabs = "\t".repeat(depth);
    println!("{}{:?}: {:?}", tabs, pair.as_rule(), pair.as_str());
    for inner_pair in pair.into_inner() {
        print_pairs(inner_pair, depth + 1);
    }
}

fn main() {
    let pairs = NumberParser::parse(
        Rule::expression,
        r#"1 + 2 * 3"#).unwrap();

    for pair in pairs {
        println!("{:?}: {:?}", pair.as_rule(), pair.as_str());

        for inner_pair in pair.into_inner() {
            print_pairs(inner_pair, 1);
        }
    }
}
