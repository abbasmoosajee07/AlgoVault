/* AquaQ Puzzles - Puzzle 0
Solution Started: September 7, 2025,
Puzzle Link: https://challenges.aquaq.co.uk/challenge/0
Solution by: Abbas Moosajee
Brief: [What's a numpad] */

use std::{fs, env, error::Error};
use std::collections::HashMap;

fn main() -> Result<(), Box<dyn Error>> {

    // Get the first command-line argument, or default to "Lang06_input.txt"
    let args: Vec<String> = env::args().collect();
    let file_path = if args.len() > 1 {
        &args[1]  // Use the provided file path
    } else {
        "../../inputs/challenge_00.txt"  // Default file
    };

    let contents = fs::read_to_string(file_path)?;


    let data: Vec<&str> = contents
        .lines()
        .map(|line| line.trim())
        .filter(|line| !line.is_empty())
        .collect();

    // build T9 dictionary
    let mut t9_dict: HashMap<i32, &str> = HashMap::new();
    t9_dict.insert(2, "abc");
    t9_dict.insert(3, "def");
    t9_dict.insert(4, "ghi");
    t9_dict.insert(5, "jkl");
    t9_dict.insert(6, "mno");
    t9_dict.insert(7, "pqrs");
    t9_dict.insert(8, "tuv");
    t9_dict.insert(9, "wxyz");
    t9_dict.insert(1, " ");
    t9_dict.insert(0, " ");

    // build message
    let mut message = String::new();
    for entry in data {
        let parts: Vec<i32> = entry
            .split_whitespace()
            .map(|s| s.parse::<i32>().unwrap())
            .collect();
        let key = parts[0];
        let press = parts[1];

        if let Some(letters) = t9_dict.get(&key) {
            if let Some(ch) = letters.chars().nth((press - 1) as usize) {
                message.push(ch);
            }
        }
    }

    println!("Challenge 00: {}", message);

    Ok(())
}
