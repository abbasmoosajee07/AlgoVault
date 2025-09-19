/* Marches And Gnatts - Quest 18
Solution Started: September 19, 2025
Puzzle Link: https://mng.quest/quest/18/
Solution by: Abbas Moosajee
Brief: [Unary Division]
*/

import { MNG_ARENA } from '../MNG_ARENA.js';

const unary_div = new MNG_ARENA("Quest18_input");

const test_rules = `// unary division
INIT | INIT | L
INIT _ MARK , R
MARK | MARK | R
MARK ÷ MARK _ R
MARK , MARK , R
MARK _ DIV _ L
DIV | DIVIDE _ L
DIVIDE | DIVIDE | L
DIVIDE _ APPLY _ L
APPLY @ APPLY @ L
APPLY | APPLIED @ R
APPLIED @ APPLIED @ R
APPLIED _ MARK _ R
DIV _ COUNT _ L
MARK @ SHIFT _ R
SHIFT @ SHIFT | R
SHIFT _ MARK | R
COUNT @ COUNT @ L
COUNT | COUNT | L
COUNT , COUNT , L
COUNT _ MARK | R
APPLY , REMAINDER , R
REMAINDER @ REMAINDER | R
REMAINDER _ CLEAN _ R
CLEAN | CLEAN _ R
CLEAN _ HALT _ R`;

unary_div.full_solution(test_rules);
unary_div.benchmark_solution(["|||÷||", "||÷||", "|||||÷|||"], false)
// unary_div.test_solution("||||||÷||||", true)
unary_div.save_rules(import.meta.url);
