/**
 * Marches And Gnatts - Puzzle 1
Puzzle Link: https://mng.quest/quest/1/unary-addition
Solution by: Abbas Moosajee
Brief: [Unary Addition]
 */

import { MNG_ARENA } from '../MNG_ARENA.js';

const unary_add_rules = `
INIT | FIND _ R
FIND | FIND | R
FIND + HALT | R
`;

const unary_add = new MNG_ARENA("unary_addition")
unary_add.full_solution(unary_add_rules);
unary_add.benchmark_solution(["|||+||||", "|+|", "|||+||||"], false)
// unary_add.test_solution("|||+||||", true)
// unary_add.save_rules(import.meta.url);
