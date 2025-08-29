/**
 * Marches And Gnatts - Puzzle 12
Solution Started: Aug 7, 2025
Puzzle Link: https://mng.quest/quest/12/decimal-addition
Solution by: Abbas Moosajee
Brief: [Decimal Addition]

 * Day 12 - Year MNG
 * Author: Abbas Moosajee
 */
import { MNG_ARENA } from '../MNG_ARENA.js';


const LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j'];
const MAX_N = 9;

const dec_add = new MNG_ARENA("Quest12_input");

// INIT rules
for (let n = 0; n <= MAX_N; n++) {
    dec_add.ignore("INIT", n, "R");
}
dec_add.ignore("INIT", "+", "R");
dec_add.add_rule("INIT", "_", "dec", "_", "L");

// dec rules
dec_add.add_rule("dec", "0", "shift", "_", "L");
for (let n = 1; n <= MAX_N; n++) {
    dec_add.add_rule("dec", n, "clean", (n-1), "L");
}
dec_add.add_rule("dec", "+", "clean", "_", "L");
dec_add.add_rule("clean", "+", "inc", "+", "L");

// shift rules
for (let n = 0; n <= MAX_N; n++) {
    dec_add.ignore("shift", n, "L");
}
dec_add.add_rule("shift", "+", "fix", "+", "L");
LETTERS.forEach(letter => {
    dec_add.add_rule("shift", letter, "fix", letter, "L");
});

// fix rules
LETTERS.forEach(letter => {
    dec_add.ignore("fix", letter, "L");
});
for (let n = 0; n <= MAX_N; n++) {
    dec_add.add_rule("fix", n, "INIT", LETTERS[n], "R");
}
dec_add.add_rule("fix", "_", "INIT", "a", "R");

// inc rules
LETTERS.forEach(letter => {
    dec_add.ignore("inc", letter, "L");
});
for (let n = 0; n < MAX_N; n++) {
    dec_add.add_rule("inc", n, "INIT", (n+1), "R");
}
dec_add.add_rule("inc", "9", "inc", "0", "L");
dec_add.add_rule("inc", "_", "INIT", "1", "R");

// repeat rules
LETTERS.forEach(letter => {
    dec_add.ignore("INIT", letter, "R");
});

// clean rules
for (let n = 0; n <= MAX_N; n++) {
    dec_add.add_rule("clean", LETTERS[n], "clean", n.toString(), "L");
    dec_add.ignore("clean", n, "L");
}
dec_add.add_rule("clean", "_", "HALT", "_", "R");

dec_add.benchmark_solution(["2+5", "14+7", "21+21"], false)
// dec_add.test_solution("2+5", true)
// dec_add.save_rules(import.meta.url);