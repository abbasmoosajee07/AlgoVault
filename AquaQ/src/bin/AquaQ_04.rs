/* AquaQ Puzzles - Puzzle 4
Solution Started: September 17, 2025,
Puzzle Link: https://challenges.aquaq.co.uk/challenge/4
Solution by: Abbas Moosajee
Brief: [This is a good coprimen] */

use std::{env, fs, io};

fn gcd(mut a: u32, mut b: u32) -> u32 {
    while b != 0 {
        let tmp = b;
        b = a % b;
        a = tmp;
    }
    a
}

fn coprimes_of(n: u32) -> Vec<u32> {
    let mut result = Vec::new();
    for i in 1..=n {
        if gcd(i, n) == 1 {
            result.push(i);
        }
    }
    result
}

fn main() -> io::Result<()> {
    let args: Vec<String> = env::args().collect();
    let file_path = if args.len() > 1 {
        &args[1]  // Use the provided file path
    } else {"inputs/challenge_04.txt"};

    let contents: String = fs::read_to_string(file_path)?;
    let n = contents.parse().expect("Not a valid number");
    let cps = coprimes_of(n);
    let coprime_sum = cps.into_iter().map(u64::from).sum::<u64>();

    println!("Challenge 04: {}", coprime_sum);
    Ok(())
}
