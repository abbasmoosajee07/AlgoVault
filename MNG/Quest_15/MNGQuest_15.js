/* Marches And Gnatts - Quest 15
Solution Started: August 29, 2025
Puzzle Link: https://mng.quest/quest/15/square-root
Solution by: Abbas Moosajee
Brief: [SQUARE ROOT]
*/

import { MNG_ARENA } from '../MNG_ARENA.js';


const sqrtTM = new MNG_ARENA("Quest15_input");


// Mark the end of the input
sqrtTM.find_state("INIT", "_", "|", "R", "START", "#", "L");

// Mark the end of the to-be-added state with I, decrementing once
sqrtTM.find_state("START", "_", "|", "L", "FIRST_2", "I", "R");
sqrtTM.add_rule("FIRST_2", "|", "NEXT_2", "2", "R");

// Go to next number to be subtracted
sqrtTM.find_state("NEXT_2", "2", new Set(["|", "_", "0"]), "L", "SUB_2", "0", "L");

// Build the subtrahend and subtract
for (let n = 2; n < 245; n++) {
    sqrtTM.add_rule(`SUB_${n}`, "2", `SUB_${n + 2}`, "0", "L");
    sqrtTM.add_rule(`SUB_${n}`, "I", `SUB_${n}`, "I", "R");

    sqrtTM.find_state(`SUB_${n}`, "|", new Set(["_", "0"]), "R", `SUB_${n - 1}`, "_", "R");

    sqrtTM.add_rule(`SUB_${n}`, "#", "FINISH", "_", "L");
}

// Base case: subtracting 1
sqrtTM.add_rule("SUB_1", "|", "NEXT_2", "_", "L");

// If end of input: increment subtrahend
sqrtTM.add_rule("NEXT_2", "I", "INC", "I", "R");

// Refresh zeroes to twos and add another two
sqrtTM.add_rule("INC", "0", "INC", "2", "R");
sqrtTM.add_rule("INC", "_", "DEC", "2", "R");

// Decrement once before continuing
sqrtTM.find_state("DEC", "|", "_", "R", "NEXT_2", "_", "L");

// If end of input while subtracting → done
for (let state of ["DEC", "NEXT_2"]) {
    sqrtTM.add_rule(state, "#", "FINISH", "_", "L");
}

// Clean up and halt
sqrtTM.ignore("FINISH", "_", "L");
sqrtTM.add_rule("FINISH", "0", "FINISH", "|", "L");
sqrtTM.add_rule("FINISH", "2", "FINISH", "|", "L");
sqrtTM.add_rule("FINISH", "I", "HALT", "_", "R");

// console.log(sqrtTM.rules);

// Test case
const testTape = "|||||||||";
sqrtTM.benchmark_solution([testTape, "|||||||||||||||||||||||||", "||||"], false)

// sqrtTM.test_solution(testTape, true);
sqrtTM.save_rules(import.meta.url);