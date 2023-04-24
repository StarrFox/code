#![no_main]

use fuzzy;

use libfuzzer_sys::fuzz_target;

fuzz_target!(|data: (u16, u16, Vec<Vec<bool>>)| {
    //fuzzy::parse_pbm(("P1".to_owned() + data).as_str());

    let (height, width, aaa) = data;
    let test = fuzzy::PBM1{height, width, data: aaa};

    fuzzy::make_pbm1_image(test);
});
