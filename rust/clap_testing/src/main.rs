use clap::Parser;

#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
    /// Name of the person to greet
    #[arg(short, long)]
    name: String
}


fn main() {
    let args = Args::parse();

    println!("name was {}", args.name);
}
