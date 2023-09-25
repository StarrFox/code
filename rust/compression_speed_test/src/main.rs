use glob::glob;
use std::fs;
use std::io;
use std::path::PathBuf;
use std::time;

// -4 to 4
const ZSTD_LEVEL: i32 = -4;
// ?
const LZ4_LEVEL: u32 = 0;

type Algo = fn(&[u8]) -> Vec<u8>;


fn main() {
    let test_data = glob("test_data/*").expect("invalid glob");

    for file_path in test_data.filter_map(|result| result.ok()) {
        test_algo(&file_path, compress_snap, decompress_snap, "snap");
        test_algo(&file_path, compress_zstd, decompress_zstd, "zstd");
        test_algo(&file_path, compress_lz4, decompress_lz4, "lz4");
        test_algo(&file_path, compress_lz4_flex, decompress_lz4_flex, "lz4_flex");
        println!();
    }
}

fn test_algo(file_path: &PathBuf, compress: Algo, decompress: Algo, algo_name: &str) {
    let file_data = open_file(&file_path);
    let file_name = file_path.file_name().unwrap().to_str().unwrap();
    let compressed_data = execute_algo(&file_data, file_name, true, algo_name, compress);
    let decompressed_data = execute_algo(&compressed_data, file_name, false, algo_name, decompress);

    assert!(decompressed_data == file_data)
}

fn open_file(path: &PathBuf) -> Vec<u8> {
    fs::read(path).expect(format!("couldn't open {path:?}").as_str())
}

fn execute_algo(file_data: &[u8], file_name: &str, compress: bool, algo_name: &str, algo: fn(&[u8]) -> Vec<u8>) -> Vec<u8> {
    let start = time::Instant::now();
    let data = algo(&file_data);
    let elapsed = start.elapsed();

    let mode = match compress {
        true => "compress",
        false => "decompress"
    };

    println!(
        "{mode}: algo={algo_name}, file={file_name} elapsed={elapsed:?} input size={} output size={}",
        file_data.len(),
        data.len(),
    );

    data
}

fn compress_snap(mut data: &[u8]) -> Vec<u8> {
    let mut writer = snap::write::FrameEncoder::new(Vec::new());
    io::copy(&mut data, &mut writer).unwrap();
    writer.into_inner().unwrap()
}

fn decompress_snap(data: &[u8]) -> Vec<u8> {
    let mut stream: Vec<u8> = Vec::new();
    let mut reader = snap::read::FrameDecoder::new(data);
    io::copy(&mut reader, &mut stream).unwrap();
    stream
}

fn compress_zstd(mut data: &[u8]) -> Vec<u8> {
    let mut writer = zstd::stream::Encoder::new(Vec::new(), ZSTD_LEVEL).unwrap();
    io::copy(&mut data, &mut writer).unwrap();
    writer.finish().unwrap()
}

fn decompress_zstd(data: &[u8]) -> Vec<u8> {
    let mut stream = Vec::new();
    let mut decoder = zstd::stream::Decoder::new(data).unwrap();
    io::copy(&mut decoder, &mut stream).unwrap();
    stream
}

fn compress_lz4(mut data: &[u8]) -> Vec<u8> {
    let mut writer = lz4::EncoderBuilder::new()
        .level(LZ4_LEVEL)
        .build(Vec::new())
        .unwrap();
    io::copy(&mut data, &mut writer).unwrap();

    writer.finish().0
}

fn decompress_lz4(data: &[u8]) -> Vec<u8> {
    let mut stream = Vec::new();
    let mut decoder = lz4::Decoder::new(data).unwrap();
    io::copy(&mut decoder, &mut stream).unwrap();

    stream
}

fn compress_lz4_flex(mut data: &[u8]) -> Vec<u8> {
    let mut writer = lz4_flex::frame::FrameEncoder::new(Vec::new());
    io::copy(&mut data, &mut writer).unwrap();
    writer.finish().unwrap()
}

fn decompress_lz4_flex(data: &[u8]) -> Vec<u8> {
    let mut stream = Vec::new();
    let mut reader = lz4_flex::frame::FrameDecoder::new(data);
    io::copy(&mut reader, &mut stream).unwrap();
    stream
}
