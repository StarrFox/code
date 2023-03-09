// fn main() {
//     let input = include_str!("input");

//     let mut current: u32 = 0;
//     let mut highest: u32 = 0;

//     for line in input.split("\n") {
//         if line.len() == 0 {
//             if current >= highest {
//                 highest = current;
//             }

//             current = 0;
//             continue;
//         }

//         let parsed: u32 = line.parse().unwrap();
//         current += parsed;
//     }

//     println!("Highest = {}", highest);
// }

// small rust
fn main() {
    let input = include_str!("input");

    let highest: u32 = input
        .split("\n\n")
        .map(|group| {
            group
                .split("\n")
                .map(|line| line.parse::<u32>().unwrap_or(0))
                .sum()
        })
        .max()
        .unwrap();

    println!("Highest = {}", highest);
}
