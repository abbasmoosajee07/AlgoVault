/* AquaQ Puzzles - Puzzle 2
Solution Started: September 9, 2025,
Puzzle Link: https://challenges.aquaq.co.uk/challenge/2
Solution by: Abbas Moosajee
Brief: [One is all you need] */

use std::{fs, env, error::Error};

fn main() -> Result<(), Box<dyn Error>> {

    // Get the first command-line argument, or default to "Lang06_input.txt"
    let args: Vec<String> = env::args().collect();
    let file_path = if args.len() > 1 {
        &args[1]  // Use the provided file path
    } else {
        "inputs/challenge_02.txt"  // Default file
    };

    let contents: String = fs::read_to_string(file_path)?;

    // Step 1: Collect bytes into Vec<i32>
    let data: Vec<i32> = contents
        .split_whitespace()
        .map(|s| s.parse::<i32>().unwrap())
        .collect();

    // Step 2: Process like Python
    let mut num_list: Vec<i32> = Vec::new();

    for value in data.iter() {
        if let Some(pos) = num_list.iter().position(|&x| x == *value) {
            // truncate everything from pos to end
            num_list.truncate(pos);
        }
        num_list.push(*value);
        // println!("{:?}", num_list);
    }


    let sum: i32 = num_list.iter().sum();
    println!("Challenge 02: {}", sum);
    Ok(())
}
