/* AquaQ Puzzles - Puzzle 6
Solution Started: September 19, 2025,
Puzzle Link: https://challenges.aquaq.co.uk/challenge/6
Solution by: Abbas Moosajee
Brief: [Let me count the Ways] */

use std::{env, fs, io};
use std::collections::HashMap;

fn triples_summing_to(n: u32) -> Vec<String> {
    let mut combos = Vec::new();
    for a in 0..=n {
        for b in 0..=n - a {
            let c = n - a - b;
            combos.push(format!("{}{}{}", a, b, c));
        }
    }
    combos
}

fn main() -> io::Result<()> {

    // Get the first command-line argument, or default to "Lang06_input.txt"
    let args: Vec<String> = env::args().collect();
    let file_path = if args.len() > 1 {
        &args[1]  // Use the provided file path
    } else {
        "inputs/challenge_06.txt"  // Default file
    };

    let contents: String = fs::read_to_string(file_path)?;
    println!("{}", contents);

    let n: u32 = 123;
    let combos: Vec<String> = triples_summing_to(n);

    let mut count: i32 = 0;
    for combo in combos {
        let mut freq: HashMap<char, i32> = HashMap::new();
        for ch in combo.chars() {
            *freq.entry(ch).or_insert(0) += 1;
        }
        count += *freq.get(&'1').unwrap_or(&0);
    }

    println!("Challenge 06: {}", count);

    Ok(())
}
