use std::io;
use std::fs;
use std::time;

// -4 to 4
const ZSTD_LEVEL: i32 =  -4;
// ?
const LZ4_LEVEL: u32 = 0;

// NOTE: could have just used the const in the functions instead of passing it
enum Algo {
    Snap(fn(&[u8], &str) -> Vec<u8>),
    Zstd(fn(&[u8], &str, i32) -> Vec<u8>),
    Lz4(fn(&[u8], &str, u32) -> Vec<u8>)
}

fn main() {
    let test_data = vec!("test_data/image.png", "test_data/richard.qoi");

    for file_name in test_data {
        test_algo(
            file_name, 
            Algo::Snap(test_compress_snap), 
            Algo::Snap(test_decompress_snap),
        );

        test_algo(
            file_name, 
            Algo::Zstd(test_compress_zstd), 
            Algo::Zstd(test_decompress_zstd),
        );

        test_algo(
            file_name,
            Algo::Lz4(test_compress_lz4),
            Algo::Lz4(test_decompress_lz4),
        );
    }

}

fn test_algo(file_name: &str, compress: Algo, decompress: Algo) {
    let file_data = open_file(file_name);
    //let compressed_data = compress(&file_data, file_name);
    let compressed_data = match compress {
        Algo::Snap(snap_compress) => snap_compress(&file_data, file_name),
        Algo::Zstd(zstd_compress) => zstd_compress(&file_data, file_name, ZSTD_LEVEL),
        Algo::Lz4(lz4_compress) => lz4_compress(&file_data, file_name, LZ4_LEVEL),
    };
    let decompressed_data = match decompress {
        Algo::Snap(snap_decompress) => snap_decompress(&compressed_data, file_name),
        Algo::Zstd(zstd_decompress) => zstd_decompress(&compressed_data, file_name, ZSTD_LEVEL),
        Algo::Lz4(lz4_decompress) => lz4_decompress(&compressed_data, file_name, LZ4_LEVEL),
    };
    println!();

    assert!(decompressed_data == file_data)
}

fn open_file(path: &str) -> Vec<u8> {
    fs::read(path).expect(format!("couldn't open {path}").as_str())
}

fn test_compress_snap(file_data: &[u8], name: &str) -> Vec<u8> {
    let start = time::Instant::now();
    let compressed_data = compress_snap(&file_data);
    let elapsed = start.elapsed();

    println!(
        "snap compress {name}:\n\telapsed: {elapsed:?}\n\tdecompressed size: {}\n\tcompressed size: {}",
        file_data.len(),
        compressed_data.len(),
    );

    compressed_data
}

fn compress_snap(mut data: &[u8]) -> Vec<u8> {
    let mut writer = snap::write::FrameEncoder::new(Vec::new());
    io::copy(&mut data, &mut writer).unwrap();
    writer.into_inner().unwrap()
}

fn test_decompress_snap(data: &[u8], name: &str) -> Vec<u8> {
    let start = time::Instant::now();
    let decompressed_data = decompress_snap(&data);
    let elapsed = start.elapsed();

    println!(
        "snap decompress {name}:\n\telapsed: {elapsed:?}\n\tcompressed size: {}\n\tdecompressed size: {}",
        data.len(),
        decompressed_data.len(),
    );

    decompressed_data
}

fn decompress_snap(data: &[u8]) -> Vec<u8> {
    let mut stream: Vec<u8> = Vec::new();
    let mut reader = snap::read::FrameDecoder::new(data);
    io::copy(&mut reader, &mut stream).unwrap();
    stream
}

fn test_compress_zstd(file_data: &[u8], name: &str, level: i32) -> Vec<u8> {
    let start = time::Instant::now();
    let compressed_data = compress_zstd(file_data, level);
    let elapsed = start.elapsed();

    println!(
        "zstd ({level}) compress {name}:\n\telapsed: {elapsed:?}\n\tdecompressed size: {}\n\tcompressed size: {}",
        file_data.len(),
        compressed_data.len()
    );

    compressed_data
}

fn compress_zstd(mut data: &[u8], level: i32) -> Vec<u8> {
    let mut writer = zstd::stream::Encoder::new(Vec::new(), level).unwrap();
    io::copy(&mut data, &mut writer).unwrap();
    writer.finish().unwrap()
}

// level isnt even used to decompress
fn test_decompress_zstd(data: &[u8], name: &str, level: i32) -> Vec<u8> {
    let start = time::Instant::now();
    let decompressed_data = decompress_zstd(&data);
    let elapsed = start.elapsed();

    println!(
        "zstd ({level}) decompress {name}:\n\telapsed: {elapsed:?}\n\tcompressed size: {}\n\tdecompressed size: {}",
        data.len(),
        decompressed_data.len()
    );

    decompressed_data
}

fn decompress_zstd(data: &[u8]) -> Vec<u8> {
    let mut stream = Vec::new();
    let mut decoder = zstd::stream::Decoder::new(data).unwrap();
    io::copy(&mut decoder, &mut stream).unwrap();
    stream
}

fn test_compress_lz4(file_data: &[u8], name: &str, level: u32) -> Vec<u8> {
    let start = time::Instant::now();
    let compressed_data = compress_lz4(file_data, level);
    let elapsed = start.elapsed();

    println!(
        "lz4 ({level}) compress {name}:\n\telapsed: {elapsed:?}\n\tdecompressed size: {}\n\tcompressed size: {}",
        file_data.len(),
        compressed_data.len(),
    );

    compressed_data
}

fn compress_lz4(mut data: &[u8], level: u32) -> Vec<u8> {
    let mut writer = lz4::EncoderBuilder::new()
        .level(level)
        .build(Vec::new())
        .unwrap();
    io::copy(&mut data, &mut writer).unwrap();

    writer.finish().0
}

fn test_decompress_lz4(data: &[u8], name: &str, level: u32) -> Vec<u8> {
    let start = time::Instant::now();
    let decompressed_data = decompress_lz4(data);
    let elapsed = start.elapsed();

    println!(
        "lz4 ({level}) decompress {name}:\n\telapsed: {elapsed:?}\n\tcompressed size: {}\n\tdecompressed size: {}",
        data.len(),
        decompressed_data.len(),
    );

    decompressed_data
}

fn decompress_lz4(data: &[u8]) -> Vec<u8> {
    let mut stream = Vec::new();
    let mut decoder = lz4::Decoder::new(data).unwrap();
    io::copy(&mut decoder, &mut stream).unwrap();

    stream
}

