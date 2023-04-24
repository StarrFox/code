use std::{
    fs::File,
    collections::HashMap,
    io::BufReader,
};
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize)]
#[serde(untagged)]
enum StrOrInt {
    Str(String),
    Int(u32),
}

#[derive(Serialize, Deserialize)]
struct Property {
    r#type: String,
    id: u32,
    offset: u32,
    flags: u32,
    container: String,
    dynamic: bool,
    singleton: bool,
    pointer: bool,
    hash: u32,
    enum_options: Option<HashMap<String, StrOrInt>>
}

#[derive(Serialize, Deserialize)]
struct Class {
    bases: Vec<String>,
    name: String,
    properties: HashMap<String, Property>,
}

#[derive(Serialize, Deserialize)]
struct TypesJson {
    version: u8,
    classes: HashMap<String, Class>,
}

fn main() {
    let file_handle = File::open("types.json").unwrap();
    let reader = BufReader::new(file_handle);
    let v: TypesJson = serde_json::from_reader(reader).unwrap();

    println!("version: {}", v.version);
}
