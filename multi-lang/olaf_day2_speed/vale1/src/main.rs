#[repr(C)]
struct AlignedTo<Align, Bytes: ?Sized> {
    _align: [Align; 0],
    bytes: Bytes, 
}

// dummy static used to create aligned data
static ALIGNED: &'static AlignedTo<u32, [u8]> = &AlignedTo {
    _align: [],
    bytes: *include_bytes!("input.txt"),
};

static INPUT: &'static [u8] = &ALIGNED.bytes;

fn main() {
    let ints: &[u32] = bytemuck::cast_slice(INPUT);

    let mut result = ints.len() as u32;
    for i in ints {
        let o = i.wrapping_mul(1887065750_u32) >> 27;
        result += (*i == 173678658) as u32 + ((475903013 >> o) & 7);
    }

    println!("{result}");
}
