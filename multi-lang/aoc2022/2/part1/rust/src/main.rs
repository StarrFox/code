fn main() {
    let input = include_str!("input");

    let mut score: u32 = 0;

    for line in input.split("\n") {
        if line.len() == 0 {
            continue;
        }

        let enemy = match line.chars().nth(0).unwrap() {
            'A' => 1,
            'B' => 2,
            'C' => 3,
            _ => panic!("Unreachable")
        };

        let me = match line.chars().nth(2).unwrap() {
            'X' => 1,
            'Y' => 2,
            'Z' => 3,
            _ => panic!("Unreachable")
        };

        // won
        if (enemy == 3 && me == 1) || (enemy < me && !(enemy == 1 && me == 3)) {
            score += 6;
        }
        // tie
        else if enemy == me {
            score += 3;
        }
        score += me;
    }

    println!("score = {}", score);
}
