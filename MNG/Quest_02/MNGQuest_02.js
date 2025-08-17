/**
 * Marches And Gnatts - Puzzle 2
Solution Started: Jul 26, 2025
Puzzle Link: https://mng.quest/quest/2/unary-even-odd
Solution by: Abbas Moosajee
Brief: [Unary Even Odd]
 */

import { MNG_ARENA } from '../MNG_ARENA.js';

const unary_eo_rules = `
INIT | ODD  _ R
ODD  | INIT _ R
ODD  _ HALT O R
INIT _ HALT E R
`;

const unary_even_odd = new MNG_ARENA("unary_even_odd")
unary_even_odd.full_solution(unary_eo_rules);
unary_even_odd.benchmark_solution(["|||||||", "|||||", "||||"], false)
// unary_even_odd.test_solution("|||||||", true)
// unary_even_odd.save_rules(import.meta.url);
