/**
 * Marches And Gnatts - Puzzle 9
Solution Started: Aug 7, 2025
Puzzle Link: https://mng.quest/quest/9/unary-comparison
Solution by: Abbas Moosajee
Brief: [Unary Comparison]

 * Day 09 - Year MNG
 * Author: Abbas Moosajee
 */


import { MNG_ARENA } from '../MNG_ARENA.js';

const MAX_N = 200;
const unary_compare = new MNG_ARENA("Quest09_input");

// Add the main rules using MNG_ARENA methods
unary_compare.ignore("CheckEqual", "|", "L");
unary_compare.ignore("CountB_0", "|", "L");
unary_compare.add_rule("CheckEqual", ">", "HALT", "=", "L");
unary_compare.add_rule("CountB_0", ">", "HALT", "<", "L");
unary_compare.add_rule("CountB_0", "_", "CheckEqual", "_", "L");
unary_compare.add_rule("INIT", "|", "CountA_1", "|", "R");

// Add the counting rules using a loop
for (let n = 1; n <= MAX_N; n++) {
    unary_compare.add_rule(`CountA_${n}`, "|", `CountA_${n + 1}`, "|", "R");
    unary_compare.add_rule(`CountA_${n}`, ",", `CountB_${n}`, ">", "R");
    unary_compare.add_rule(`CountB_${n}`, "_", "HALT", "_", "L");
    unary_compare.add_rule(`CountB_${n}`, "|", `CountB_${n - 1}`, "|", "R");
}

unary_compare.benchmark_solution(["||||,||", "|||,||||", "|||,|||"], false)
// unary_compare.test_solution("||||,||", true)
// unary_compare.save_rules(import.meta.url);
