/**
 * Marches And Gnatts - Puzzle 6
Solution Started: Aug 6, 2025
Puzzle Link: https://mng.quest/quest/6/unary-subtraction
Solution by: Abbas Moosajee
Brief: [Unary Subtraction]

 */

import { MNG_ARENA } from '../MNG_ARENA.js';

const MAX_N = 100;
const unary_sub = new MNG_ARENA("unary_subtraction");

// Starting rule
unary_sub.add_rule("INIT", "|", "Count_1", "_", "R");

for (let n = 1; n <= MAX_N; n++) {
    // Count bars
    unary_sub.add_rule(`Count_${n}`, "|", `Count_${n + 1}`, "_", "R");

    // When hitting subtraction marker "-"
    unary_sub.add_rule(`Count_${n}`, "-", `Sub_${n}`, "_", "R");

    if (n - 1 > 0) {
        // Perform subtraction
        unary_sub.add_rule(`Sub_${n}`, "|", `Sub_${n - 1}`, "_", "R");
        unary_sub.add_rule(`Sub_${n}`, "_", `Sub_${n - 1}`, "|", "R");
    } else {
        // When result is zero, HALT
        unary_sub.add_rule(`Sub_${n}`, "_", "HALT", "|", "R");
        unary_sub.add_rule(`Sub_${n}`, "|", "HALT", "_", "R");
    }
}

unary_sub.benchmark_solution(["|||||-||", "|||-||", "|-|"], false)
// unary_sub.test_solution("|||||-||", true)
// unary_sub.save_rules(import.meta.url);
