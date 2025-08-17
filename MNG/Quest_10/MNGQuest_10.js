/**
 * Marches And Gnatts - Puzzle 10
Solution Started: Aug 7, 2025
Puzzle Link: https://mng.quest/quest/10/lines-count
Solution by: Abbas Moosajee
Brief: [Lines Count]

 * Day 10 - Year MNG
 * Author: Abbas Moosajee
 */
import { MNG_ARENA } from '../MNG_ARENA.js';
const line_counter = new MNG_ARENA("lines_count");
const all_letters = "abcdefghijklmnopqrstuvwxyzäöõü-";
const MAX_N = 699;

// Add rules for each letter
for (const char of all_letters) {
    line_counter.add_rule("INIT", char, "INIT", ".", "R");
}

// Special character rules
line_counter.add_rule("INIT", "+", "INIT", "|", "R");
line_counter.add_rule("INIT", "_", "Count_1", "_", "L");

// Counting rules
for (let n = 1; n <= MAX_N; n++) {
    line_counter.add_rule(`Count_${n}`, ".", `Count_${n}`, "_", "L");
    line_counter.add_rule(`Count_${n}`, "|", `Count_${n + 1}`, "_", "L");

    if (n === 1) {
        line_counter.add_rule(`Count_${n}`, "_", "HALT", "|", "L");
    } else {
        line_counter.add_rule(`Count_${n}`, "_", `Count_${n - 1}`, "|", "L");
    }
}

const test_tape  = "hello+world+how-are-you"

line_counter.benchmark_solution([test_tape, "cricket+is+great", "i+love+nutella"], false)
// line_counter.test_solution(test_tape, true)
// line_counter.save_rules(import.meta.url);