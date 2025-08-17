/**
* Marches And Gnatts - Puzzle 8
Solution Started: Aug 7, 2025
Puzzle Link: https://mng.quest/quest/8/text-mirror
Solution by: Abbas Moosajee
Brief: [Text Mirror]
*/

import { MNG_ARENA } from '../MNG_ARENA.js';

const text_mirror = new MNG_ARENA("text_mirror");
const valid_letters = "abcdefghijklmnopqrstuvwxyzäöõü-";
const extra_symbols = ":.";

// Add initial comment
text_mirror.add_comment("hello-world");

// Add the main rules
text_mirror.add_rule("INIT", "_", "MOVE_L", ":", "L");
text_mirror.add_rule("IGNORE", ":", "MOVE_L", ":", "L");
text_mirror.add_rule("MOVE_L", ".", "MOVE_L", ".", "L");
text_mirror.add_rule("MOVE_L", "_", "Final", "_", "R");
text_mirror.add_rule("Final", ".", "Final", "_", "R");
text_mirror.add_rule("Final", ":", "HALT", "_", "R");

// Add rules for each valid letter
for (const char of valid_letters) {
    // INIT state transitions
    text_mirror.ignore("INIT", char, "R");

    // MOVE_L transitions
    text_mirror.add_rule("MOVE_L", char, `COPY_${char}`, ".", "R");

    // COPY and IGNORE transitions
    text_mirror.add_rule(`COPY_${char}`, "_", "IGNORE", char, "L");
    text_mirror.ignore("IGNORE", char, "L");

    // COPY character transitions for all valid letters and symbols
    for (const ig_char of valid_letters + extra_symbols) {
        text_mirror.ignore(`COPY_${char}`, ig_char, "R");
    }
}


const test_tape  = "hello-world"

text_mirror.benchmark_solution([test_tape, "avogadro", "turing-machine"], false)
// text_mirror.test_solution(test_tape, true)
// text_mirror.save_rules(import.meta.url);
