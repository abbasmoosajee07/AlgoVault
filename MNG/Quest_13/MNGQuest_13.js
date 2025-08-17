/**
 * Marches And Gnatts - Puzzle 13
Solution Started: Aug 15, 2025
Puzzle Link: https://mng.quest/quest/13/unary-array-sort
Solution by: Abbas Moosajee
Brief: [Unary Sort]

 * Day 13 - Year MNG
 * Author: Abbas Moosajee
 */

import { MNG_ARENA } from '../MNG_ARENA.js';

const unarySortTM = new MNG_ARENA("unary_sort");
const MAX_NUMBER_SIZE = 357;

// ==== INITIALIZATION ====
unarySortTM.ignore("INIT", "|", "R");
unarySortTM.ignore("INIT", ",", "R");
unarySortTM.add_rule("INIT", "_", "RETURN", "H", "L");

unarySortTM.ignore("RETURN", "|", "L");
unarySortTM.ignore("RETURN", ",", "L");
unarySortTM.add_rule("RETURN", "_", "DO_COMPARE", "_", "R");

// ==== GOBACK LOGIC ====
unarySortTM.add_rule("GOBACK", ",", "RETURN", "H", "L");
unarySortTM.ignore("GOBACK", "|", "L");
unarySortTM.add_rule("GOBACK", "_", "CLEANUP", "_", "R");

// ==== CLEANUP ====
unarySortTM.ignore("CLEANUP", "|", "R");
unarySortTM.ignore("CLEANUP", ",", "R");
unarySortTM.add_rule("CLEANUP", "_", "REMOVE_LAST_COMMA", "_", "L");
unarySortTM.add_rule("REMOVE_LAST_COMMA", ",", "HALT", "_", "R");

// ==== COMPARISON AND SWAPPING LOGIC ====
// Load left number into state
for (let count = 1; count < MAX_NUMBER_SIZE; count++) {
    unarySortTM.add_rule(`LEFT_${count}`, "H", "GOBACK", ",", "L");
    
    if (count === 1) {
        unarySortTM.add_rule("DO_COMPARE", "|", "LEFT_1", "|", "R");
    } else {
        unarySortTM.add_rule(`LEFT_${count-1}`, "|", `LEFT_${count}`, "|", "R");
    }
    
    unarySortTM.add_rule(`LEFT_${count}`, ",", `COMPARE_${count}`, ",", "R");
    
    // Compare with right number
    if (count > 0) {
        unarySortTM.add_rule(`COMPARE_${count}`, "|", `COMPARE_${count-1}`, "|", "R");
    }
    unarySortTM.add_rule(`COMPARE_${count}`, ",", "SWAP_NUMBERS", ",", "L");
    unarySortTM.add_rule(`COMPARE_${count}`, "H", "SWAP_NUMBERS", "H", "L");
}

// Numbers are in correct order
unarySortTM.add_rule("COMPARE_0", ",", "SKIP_SWAP", ",", "L");
unarySortTM.add_rule("COMPARE_0", "|", "SKIP_SWAP", "|", "L");
unarySortTM.add_rule("COMPARE_0", "H", "GOBACK", ",", "L");

// Skip swap and move to next pair
unarySortTM.ignore("SKIP_SWAP", "|", "L");
unarySortTM.add_rule("SKIP_SWAP", ",", "DO_COMPARE", ",", "R");

// ==== SWAP LOGIC ====
// Mark right number with asterisks
unarySortTM.add_rule("SWAP_NUMBERS", "|", "SWAP_NUMBERS", "~", "L");
unarySortTM.add_rule("SWAP_NUMBERS", ",", "MARK_RIGHT_NUMBER", ",", "R");

// Replace asterisks with original right number
unarySortTM.ignore("MARK_RIGHT_NUMBER", "|", "R");
unarySortTM.add_rule("MARK_RIGHT_NUMBER", "~", "FIND_LEFT_COMMA", "|", "L");

// Find comma between numbers
unarySortTM.ignore("FIND_LEFT_COMMA", "|", "L");
unarySortTM.add_rule("FIND_LEFT_COMMA", ",", "FIND_LEFT_NUMBER", ",", "L");

// Find left number to swap
unarySortTM.ignore("FIND_LEFT_NUMBER", "|", "L");
unarySortTM.ignore("FIND_LEFT_NUMBER", "#", "L");
unarySortTM.add_rule("FIND_LEFT_NUMBER", ",", "MARK_LEFT_NUMBER", ",", "R");
unarySortTM.add_rule("FIND_LEFT_NUMBER", "_", "MARK_LEFT_NUMBER", "_", "R");

// Mark left number with bangs
unarySortTM.add_rule("MARK_LEFT_NUMBER", "|", "FIND_RIGHT_NUMBER", "#", "R");
unarySortTM.ignore("MARK_LEFT_NUMBER", "#", "R");
unarySortTM.ignore("FIND_RIGHT_NUMBER", "|", "R");
unarySortTM.add_rule("FIND_RIGHT_NUMBER", ",", "MARK_RIGHT_NUMBER", ",", "R");

unarySortTM.add_rule("MARK_RIGHT_NUMBER", ",", "FINISH_SWAP", ",", "L");
unarySortTM.add_rule("MARK_RIGHT_NUMBER", "H", "FINISH_SWAP", "H", "L");

// Complete the swap process
unarySortTM.ignore("FINISH_SWAP", "|", "L");
unarySortTM.ignore("FINISH_SWAP", ",", "L");
unarySortTM.add_rule("FINISH_SWAP", "#", "PLACE_NEW_COMMA", "#", "R");
unarySortTM.add_rule("PLACE_NEW_COMMA", "|", "REMOVE_OLD_COMMA", ",", "R");

// Clean up old comma
unarySortTM.ignore("REMOVE_OLD_COMMA", "|", "R");
unarySortTM.add_rule("REMOVE_OLD_COMMA", ",", "FIND_HASH", "|", "L");

// Remove temporary marks
unarySortTM.ignore("FIND_HASH", "|", "L");
unarySortTM.ignore("FIND_HASH", ",", "L");
unarySortTM.add_rule("FIND_HASH", "#", "REMOVE_HASH", "|", "L");

// Final cleanup
unarySortTM.add_rule("REMOVE_HASH", "#", "REMOVE_HASH", "|", "L");
unarySortTM.add_rule("REMOVE_HASH", ",", "CONTINUE_SORTING", ",", "R");
unarySortTM.add_rule("REMOVE_HASH", "_", "CONTINUE_SORTING", "_", "R");

// Continue with next comparison
unarySortTM.ignore("CONTINUE_SORTING", "|", "R");
unarySortTM.add_rule("CONTINUE_SORTING", ",", "DO_COMPARE", ",", "R");

// Test case
const testTape = "||,|,|||||,||||||||";
unarySortTM.benchmark_solution([testTape, "||,|||,|", "||||||,|||,||||||||||||||||||||||||||"], false)

// unarySortTM.test_solution(testTape, true);
// unarySortTM.save_rules(import.meta.url);