use image::{ImageBuffer, Rgb};

#[derive(Debug)]
pub struct PBM1 {
    pub width: u16,
    pub height: u16,
    pub data: Vec<Vec<bool>>,
}

pub fn parse_pbm1(rest: &str) -> Option<PBM1> {
    let (width, rest) = rest.split_once([' ', '\n'])?;
    let (height, rest) = rest.split_once([' ', '\n'])?;

    // this u16 is to cap the max size of images
    let width: u16 = width.trim().parse().ok()?;
    let height: u16 = height.trim().parse().ok()?;

    let mut data = vec![Vec::with_capacity(height as usize); width as usize];

    let mut rest = rest.to_string();
    rest.retain(|c| c == '0' || c == '1');

    if rest.len() != height as usize * width as usize {
        return None;
    }

    rest.chars()
        .enumerate()
        .for_each(|(position, pixel)| data[position % width as usize].push(pixel == '1'));

    Some(PBM1 {width, height, data})
}

pub fn parse_pbm(pbm: &str) -> Option<PBM1> {
    if pbm.len() < 2 {
        return None;
    }

    if !pbm.starts_with("P1") {
        return None;
    }

    let (pbm_type, rest) = pbm.split_at(2);

    match pbm_type {
        "P1" => parse_pbm1(rest.strip_prefix([' ', '\n'])?),
        _ => None,
    }
}

pub fn make_pbm1_image(pmb1: PBM1) {
    let mut imgbuf = ImageBuffer::new(pmb1.width as u32, pmb1.height as u32);

    for (x, y, pixel) in imgbuf.enumerate_pixels_mut() {
        let color: Rgb<u8> = match pmb1.data[x as usize][y as usize] {
            true => Rgb([0, 0, 0]),
            false => Rgb([255, 255, 255]),
        };

        *pixel = color;
    }

    //imgbuf.save("output.png").unwrap();
}

// fn main() {
//     let input = r#"P1
// 6 10
// 000010000010000010000010000010000010100010011100000000000000"#;

//     match parse_pbm(input) {
//         Some(parsed) => {
//             println!("parsed: {parsed:?}");
//             make_pbm1_image(parsed);
//         }
//         None => println!("Parsing failed!"),
//     }
// }
