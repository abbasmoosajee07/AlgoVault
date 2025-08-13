/**
 * Marches And Gnatts - Puzzle 0
Solution Started: Jul 25, 2025
Puzzle Link: https://mng.quest/quest/tutorial
Solution by: Abbas Moosajee
Brief: [Binary Increment]
 */
import { MNG_ARENA } from '../MNG_ARENA.js';

const unary_inc_rules = `
INIT | FIND | R
FIND | FIND | R
FIND _ HALT | R
`;

const unary_inc = new MNG_ARENA("unary_increment")
unary_inc.full_solution(unary_inc_rules);
unary_inc.benchmark_solution(["||||", "||", "|||"], false)
// unary_inc.test_solution("||||", true)
// unary_inc.save_rules(import.meta.url);

