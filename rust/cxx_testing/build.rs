fn main() -> miette::Result<()> {
    let path = std::path::PathBuf::from("external/cpr/cpr");
    let self_path = std::path::PathBuf::from("src");

    autocxx_build::Builder::new("src/main.rs", [&path, &self_path]).build()?;
    Ok(())
}