/* Marches And Gnatts - Quest 17
Solution Started: September 13, 2025
Puzzle Link: https://mng.quest/quest/17/
Solution by: Abbas Moosajee
Brief: [Code/Problem Description]
*/
import { MNG_ARENA } from '../MNG_ARENA.js';

const dec_inc_rules = `// Cellular automata
INIT + INIT + L
INIT - INIT - L

INIT _ E_DEAD 5 R

E_DEAD - E_DEAD - R
E_DEAD + E_D_SEEN_A + L
E_DEAD _ INIT _ L

E_REV + E_ALIVE + R

E_ALIVE - E_DEAD + R
E_ALIVE + E_A_SEEN_A - L
E_ALIVE _ INIT + L

E_D_SEEN_A - E_REV + R
E_D_SEEN_A 1 E_REV 6 R
E_D_SEEN_A 2 E_REV 7 R
E_D_SEEN_A 3 E_REV 8 R
E_D_SEEN_A 4 E_REV 9 R
E_D_SEEN_A 5 E_REV 0 R
E_D_SEEN_A + E_REV - R

E_A_SEEN_A + E_KILL - R
E_A_SEEN_A - E_KILL - R

E_KILL - E_ALIVE - R

INIT 1 STRIP _ R
INIT 6 STRIP + L
INIT 2 E_DEAD 1 R
INIT 7 RST2 + L
RST2 _ E_DEAD 1 R
INIT 3 E_DEAD 2 R
INIT 8 RST3 + L
RST3 _ E_DEAD 2 R
INIT 4 E_DEAD 3 R
INIT 9 RST4 + L
RST4 _ E_DEAD 3 R
INIT 5 E_DEAD 4 R
INIT 0 RST5 + L
RST5 _ E_DEAD 4 R

STRIP - STRIP _ R
STRIP + HALT + R
STRIP _ HALT _ R
`;

const cell_life = new MNG_ARENA("Quest17_input")
cell_life.full_solution(dec_inc_rules);
cell_life.benchmark_solution(["+", "+++", "+-+-++"], false)
// cell_life.test_solution("+", true)
// cell_life.save_rules(import.meta.url);
