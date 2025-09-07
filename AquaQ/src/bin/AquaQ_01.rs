/* AquaQ Puzzles - Puzzle 1
Solution Started: September 72025,
Puzzle Link: https://challenges.aquaq.co.uk/challenge/1
Solution by: Abbas Moosajee
Brief: [Rose by any other name] */

use std::{fs, env, error::Error};
use std::collections::HashSet;

const HEXADECIMAL_CHARS: &str = "0123456789abcdef";

/// Replace non-hex chars with '0'
fn to_hex_string(s: &str) -> String {
    let hexset: HashSet<char> = HEXADECIMAL_CHARS.chars().collect();
    s.chars()
        .map(|c| if hexset.contains(&c) { c } else { '0' })
        .collect()
}

/// Pad string length to nearest multiple of 3
fn pad_to_next_multiple_of_3(s: &str, pad_char: char) -> String {
    let pad_len = (3 - (s.len() % 3)) % 3;
    let mut result = String::from(s);
    for _ in 0..pad_len {
        result.push(pad_char);
    }
    result
}

/// Process string: sanitize, pad, split, and join
fn process_string(data: &str) -> String {
    let hex_chars = to_hex_string(data);
    let padded = pad_to_next_multiple_of_3(&hex_chars, 'X');
    let split_size = padded.len() / 3;

    padded
        .as_bytes()
        .chunks(split_size)
        .map(|chunk| {
            let part: String = chunk.iter().map(|&b| b as char).collect();
            part.chars().take(2).collect::<String>()
        })
        .collect::<Vec<String>>()
        .join("")
}

fn main() -> Result<(), Box<dyn Error>> {

    // Get the first command-line argument, or default to "Lang06_input.txt"
    let args: Vec<String> = env::args().collect();
    let file_path = if args.len() > 1 {
        &args[1]  // Use the provided file path
    } else {
        "../../inputs/challenge_01.txt"  // Default file
    };

    let contents = fs::read_to_string(file_path)?;

    let data: Vec<&str> = contents
        .lines()
        .map(|line| line.trim())
        .filter(|line| !line.is_empty())
        .collect();

    let final_string = process_string(data[0]);
    println!("Challenge 01: {}", final_string);

    Ok(())
}
