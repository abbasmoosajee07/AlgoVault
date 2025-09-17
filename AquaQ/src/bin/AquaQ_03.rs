/* AquaQ Puzzles - Puzzle 3
Solution Started: September 13, 2025,
Puzzle Link: https://challenges.aquaq.co.uk/challenge/3
Solution by: Abbas Moosajee
Brief: [Short Walks] */

use std::{env, fs, io};
use std::collections::HashMap;

fn build_grid_dict(grid: &str) -> HashMap<(usize, usize), char> {
    let mut grid_dict = HashMap::new();

    for (row_no, row_data) in grid.lines().enumerate() {
        for (col_no, cell) in row_data.chars().enumerate() {
            if cell == '#' {
                grid_dict.insert((row_no, col_no), cell);
            }
        }
    }

    grid_dict
}

fn main() -> io::Result<()> {

    // Get the first command-line argument, or default to "Lang06_input.txt"
    let args: Vec<String> = env::args().collect();
    let file_path = if args.len() > 1 {
        &args[1]  // Use the provided file path
    } else {"inputs/challenge_03.txt"};

    let contents: String = fs::read_to_string(file_path)?;
    let grid: &'static str = "  ##\n ####\n######\n######\n ####\n  ##";
    let grid_dict: HashMap<(usize, usize), char> = build_grid_dict(grid);
    let mut pos: (i32, i32) = (0_i32, 2_i32);
    let mut total: i32 = 0_i32;

    for ch in contents.chars() {
        let (row, col) = pos;
        let mut new_pos: (i32, i32) = pos;

        match ch {
            'U' => new_pos = (row - 1, col),
            'D' => new_pos = (row + 1, col),
            'L' => new_pos = (row, col - 1),
            'R' => new_pos = (row, col + 1),
            _ => {}
        }

        if grid_dict.contains_key(&(new_pos.0 as usize, new_pos.1 as usize)) {
            pos = new_pos;
        }
        total += pos.0 + pos.1;
    }

    println!("Challenge 03: {}", total);

    Ok(())
}
