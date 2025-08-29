/**
 * Marches And Gnatts - Puzzle 11
Solution Started: Aug 7, 2025
Puzzle Link: https://mng.quest/quest/11/decimal-increment
Solution by: Abbas Moosajee
Brief: [Decimal Increment]

 * Day 11 - Year MNG
 * Author: Abbas Moosajee
 */

import { MNG_ARENA } from '../MNG_ARENA.js';

const dec_inc_rules = `// Decimal Increment
INIT 0 INIT 0 R
INIT 1 INIT 1 R
INIT 2 INIT 2 R
INIT 3 INIT 3 R
INIT 4 INIT 4 R
INIT 5 INIT 5 R
INIT 6 INIT 6 R
INIT 7 INIT 7 R
INIT 8 INIT 8 R
INIT 9 INIT 9 R
INIT _ NUM  _ L

NUM  0 HALT 1 R
NUM  1 HALT 2 R
NUM  2 HALT 3 R
NUM  3 HALT 4 R
NUM  4 HALT 5 R
NUM  5 HALT 6 R
NUM  6 HALT 7 R
NUM  7 HALT 8 R
NUM  8 HALT 9 R
NUM  9 NUM  0 L
NUM  _ HALT 1 R
`;

const dec_inc = new MNG_ARENA("Quest11_input")
dec_inc.full_solution(dec_inc_rules);
dec_inc.benchmark_solution(["13", "41", "69"], false)
// dec_inc.test_solution("13", true)
// dec_inc.save_rules(import.meta.url);
