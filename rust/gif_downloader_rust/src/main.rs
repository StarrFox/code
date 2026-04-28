use regex::Regex;
use reqwest;
use std::fs;
use std::path::PathBuf;
use std::str::FromStr;

fn get_tenor_inner_gif(client: &reqwest::blocking::Client, url: reqwest::Url) -> Option<String> {
    let response = client.get(url).send().ok()?.text().ok()?;
    let tenor_regex = Regex::new(r#"class="Gif"[^<]+<img src="([^"]+)""#).ok()?;
    Some(tenor_regex.captures(&response)?.get(1)?.as_str().to_owned())
}

fn main() {
    let client = reqwest::blocking::Client::new();
    let output = PathBuf::from("./output");
    fs::create_dir(output.clone()).ok();

    let source = fs::read_to_string("source.txt").expect("Missing source.txt file");

    for url_str in source.lines() {
        let mut url =
            reqwest::Url::from_str(url_str.trim()).expect(&format!("Unable to parse {url_str} as url"));
        let output_path = if let Some(file_name) = url.path().split("/").last() {
            output.join(file_name).with_extension("gif")
        } else {
            continue;
        };

        if url.host_str().unwrap() == "tenor.com" {
            if let Some(inner_gif) = get_tenor_inner_gif(&client, url) {
                url = reqwest::Url::from_str(&inner_gif).unwrap();
            } else {
                continue;
            }
        }

        match client.get(url).send() {
            Ok(response) => match response.bytes() {
                Ok(content) => {
                    fs::write(output_path, content).expect("Failed to write content");
                }
                Err(error) => println!("Failed to get bytes from response: {error}"),
            },
            Err(error) => println!("Failed processing {output_path:?}, got error {error}"),
        }
    }
}
