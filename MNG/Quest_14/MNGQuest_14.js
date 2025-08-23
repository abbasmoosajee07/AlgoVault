/* Marches And Gnatts - Quest 14
Solution Started: August 23, 2025
Puzzle Link: https://mng.quest/leaderboard/quest/14/binary-to-decimal
Solution by: Abbas Moosajee
Brief: [Binary to Decimal]
*/

import { MNG_ARENA } from '../MNG_ARENA.js';

const dec_inc_rules = `// binary to decimal
INIT 0 START_COUNT 0 R
INIT 1 START_COUNT 1 R
START_COUNT _ HALT _ R
START_COUNT 0 CONTINUE 0 R
START_COUNT 1 CONTINUE 1 R
CONTINUE 0 CONTINUE 0 R
CONTINUE 1 CONTINUE 1 R
CONTINUE _ INC_BIN _ L
GO_START _ START_COUNT _ R
GO_START 1 GO_START 1 R
GO_START 0 GO_START 0 R
INC_BIN 1 INC_BIN2 0 L
INC_BIN 0 INC_BIN 1 L
INC_BIN _ CLEAN _ R
INC_BIN2 1 INC_BIN2 1 L
INC_BIN2 0 INC_BIN2 0 L
INC_BIN2 _ INC_DEC _ L
INC_DEC 0 GO_START 1 R
INC_DEC 1 GO_START 2 R
INC_DEC 2 GO_START 3 R
INC_DEC 3 GO_START 4 R
INC_DEC 4 GO_START 5 R
INC_DEC 5 GO_START 6 R
INC_DEC 6 GO_START 7 R
INC_DEC 7 GO_START 8 R
INC_DEC 8 GO_START 9 R
INC_DEC 9 INC_DEC 0 L
INC_DEC _ GO_START 1 R
CLEAN 1 CLEAN _ R
CLEAN _ HALT _ L
`;

const bin_dec = new MNG_ARENA("bin_to_dec")
bin_dec.full_solution(dec_inc_rules);
bin_dec.benchmark_solution(["1010", "1111", "101010110001"], false)
// bin_dec.test_solution("1010", true)
bin_dec.save_rules(import.meta.url);
