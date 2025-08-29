/**
 * Marches And Gnatts - Puzzle 7
Solution Started: Aug 7, 2025
Puzzle Link: https://mng.quest/quest/7/letter-mark
Solution by: Abbas Moosajee
Brief: [Letter Mark]

 * Day 07 - Year MNG
 * Author: Abbas Moosajee
 */
import { MNG_ARENA } from '../MNG_ARENA.js';


const letter_mark = new MNG_ARENA("Quest07_input");
const valid_letters = "abcdefghijklmnopqrstuvwxyzäöõü-";
const extra_symbols = "[]:";

// Add the initial comment
letter_mark.add_comment("wõta-wastu-mu-soow-ja-chillitse-toomemäel");

letter_mark.add_rule("MARK_w", "_", "MARK_w1", "[", "R");
letter_mark.add_rule("MARK_w1", "_", "MARK_w2", "w", "R");
letter_mark.add_rule("MARK_w2", "_", "GO_START", "]", "L");
letter_mark.add_rule("GO_START", "_", "START", "_", "R");
letter_mark.add_rule("MARK_ch", "h", "MARK_ch", "_", "R");
letter_mark.add_rule("MARK_ch", "_", "MARK_ch1", "[", "R");
letter_mark.add_rule("MARK_ch1", "_", "MARK_ch2", "c", "R");
letter_mark.add_rule("MARK_ch2", "_", "MARK_ch3", "h", "R");
letter_mark.add_rule("MARK_ch3", "_", "GO_START", "]", "L");
letter_mark.add_rule("START", ":", "HALT", "_", "R");
letter_mark.add_rule("INIT", "_", "GO_START", ":", "L");

// INIT state transitions
for (const char of valid_letters) {
    letter_mark.ignore("INIT", char, "R");

    if (char === "w") {
        letter_mark.add_rule("START", "w", "MARK_w", "_", "R");
    } else if (char === "c") {
        letter_mark.add_rule("START", "c", "MARK_ch", "_", "R");
    } else {
        letter_mark.add_rule("START", char, `COPY_${char}`, "_", "R");

        for (const copy_char of valid_letters + extra_symbols) {
            letter_mark.ignore(`COPY_${char}`, copy_char, "R");
        }
        letter_mark.add_rule(`COPY_${char}`, "_", "GO_START", char, "L");
    }
}

// Additional rules for extra characters
for (const extra_char of valid_letters + extra_symbols) {
    letter_mark.ignore("GO_START", extra_char, "L");
    letter_mark.ignore("MARK_w", extra_char, "R");
    if (extra_char !== "h") {
        letter_mark.ignore("MARK_ch", extra_char, "R");
    }
}


const test_tape  = "wõta-wastu-mu-soow-ja-chillitse-toomemäel"

letter_mark.benchmark_solution([test_tape, "w-uroiwjefw", "wow"], false)
// letter_mark.test_solution(test_tape, true)
// letter_mark.save_rules(import.meta.url);



