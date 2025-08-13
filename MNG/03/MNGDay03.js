/**
 * Marches And Gnatts - Puzzle 3
Solution Started: Jul 27, 2025
Puzzle Link: https://mng.quest/quest/3/binary-increment
Solution by: Abbas Moosajee
Brief: [Binary Increment]
 */


import { MNG_ARENA } from '../MNG_ARENA.js';

const binary_inc_rules = `
INIT 0 INIT 0 R
INIT 1 INIT 1 R
INIT _ FIND _ L
FIND 1 FIND 0 L
FIND 0 HALT 1 R
FIND _ HALT 1 R
`;

const binary_inc = new MNG_ARENA("unary_binary_inc")
binary_inc.full_solution(binary_inc_rules);
binary_inc.benchmark_solution(["1010", "111", "1011"], false)
// binary_inc.test_solution("1010", true)
// binary_inc.save_rules(import.meta.url);
