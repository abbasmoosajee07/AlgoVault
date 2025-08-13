/**
 * Marches And Gnatts - Puzzle 5
Solution Started: Aug 6, 2025
Puzzle Link: https://mng.quest/quest/5/find-element-in-unary-array
Solution by: Abbas Moosajee
Brief: [Find Element in Unary Array]

 * Day 05 - Year MNG
 * Author: Abbas Moosajee
 */
import { MNG_ARENA } from '../MNG_ARENA.js';


const MAX_N = 44;
const unary_array = new MNG_ARENA("unary_array");

// INIT rule
unary_array.add_rule("INIT", "|", "Count_1", "_", "R");

// Build rules for counting & finding
for (let n = 1; n <= MAX_N; n++) {
    // Skip unary bars
    unary_array.add_rule(`Count_${n}`, "|", `Count_${n + 1}`, "_", "R");

    // Found target marker ":"
    unary_array.add_rule(`Count_${n}`, ":", `Find_${n}`, "_", "R");

    // HALT when nothing else
    unary_array.add_rule(`Find_${n}`, "_", "HALT", "_", "R");

    // Bar handling in Find state
    if (n === 1) {
        unary_array.ignore(`Find_${n}`, "|", "R");
    } else {
        unary_array.add_rule(`Find_${n}`, "|", `Find_${n}`, "_", "R");
    }

    // Comma handling in Find state
    if (n - 1 === 0) {
        unary_array.add_rule(`Find_${n}`, ",", "ERASE_ALL", "_", "R");
    } else {
        unary_array.add_rule(`Find_${n}`, ",", `Find_${n - 1}`, "_", "R");
    }
}

// Cleanup rules: ERASE_ALL wipes everything
unary_array.add_rule("ERASE_ALL", "|", "ERASE_ALL", "_", "R");
unary_array.add_rule("ERASE_ALL", ",", "ERASE_ALL", "_", "R");
unary_array.add_rule("ERASE_ALL", "_", "HALT", "_", "R");

unary_array.benchmark_solution(["||:|||,|||||,||||||||,||||", "||:|,||", "|:|"], false)
// unary_array.test_solution("||:|||,|||||,||||||||,||||", true)
// unary_array.save_rules(import.meta.url);
