/* AquaQ Puzzles - Puzzle 5
Solution Started: September 19, 2025,
Puzzle Link: https://challenges.aquaq.co.uk/challenge/5
Solution by: Abbas Moosajee
Brief: [Snake Eyes] */

use std::{env, fs, io};
use std::collections::HashMap;

fn face_sum(val: i32) -> i32 {
    7 - val
}

fn spin_dice(dice: &HashMap<&str, i32>, spin: char) -> HashMap<&'static str, i32> {
    let mut new_dice = HashMap::new();

    match spin {
        'L' => {
            new_dice.insert("Left", *dice.get("Front").unwrap());
            new_dice.insert("Front", face_sum(*dice.get("Left").unwrap()));
            new_dice.insert("Top", *dice.get("Top").unwrap());
        }
        'R' => {
            new_dice.insert("Top", *dice.get("Top").unwrap());
            new_dice.insert("Left", face_sum(*dice.get("Front").unwrap()));
            new_dice.insert("Front", *dice.get("Left").unwrap());
        }
        'U' => {
            new_dice.insert("Front", *dice.get("Top").unwrap());
            new_dice.insert("Left", *dice.get("Left").unwrap());
            new_dice.insert("Top", face_sum(*dice.get("Front").unwrap()));
        }
        'D' => {
            new_dice.insert("Front", face_sum(*dice.get("Top").unwrap()));
            new_dice.insert("Left", *dice.get("Left").unwrap());
            new_dice.insert("Top", *dice.get("Front").unwrap());
        }
        _ => {}
    }

    new_dice
}

fn main() -> io::Result<()> {

    let args: Vec<String> = env::args().collect();
    let file_path = if args.len() > 1 {
        &args[1]  // Use the provided file path
    } else {"inputs/challenge_05.txt"};

    let instructions: String = fs::read_to_string(file_path)?;
    let mut dice_1: HashMap<&'static str, i32> = HashMap::from([
        ("Front", 1),
        ("Left", 2),
        ("Top", 3),
    ]);

    let mut dice_2: HashMap<&'static str, i32> = HashMap::from([
        ("Front", 1),
        ("Left", 3),
        ("Top", 2),
    ]);

    // let instructions = "LRDLU";
    let target_face: &'static str = "Front";
    let mut match_face: usize = 0;

    for (idx, instr) in instructions.chars().enumerate() {
        dice_1 = spin_dice(&dice_1, instr);
        dice_2 = spin_dice(&dice_2, instr);

        if dice_1[target_face] == dice_2[target_face] {
            match_face += idx;
        }
    }

    println!("Challenge 05: {}", match_face);
    Ok(())
}
