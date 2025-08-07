/**
 * Marches And Gnatts - Puzzle 9
Solution Started: Aug 7, 2025
Puzzle Link: https://mng.quest/quest/9/unary-comparison
Solution by: Abbas Moosajee
Brief: [Unary Comparison]

 * Day 09 - Year MNG
 * Author: Abbas Moosajee
 */


import { TuringConfig, MachineLogic } from '../TuringMachineSim/javascript_machine/TuringBrain.js';
import { TuringMachine } from '../TuringMachineSim/javascript_machine/BasicRunner.js';

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const MAX_N = 200;
const lines = [];

lines.push("CheckEqual | CheckEqual | L");                   // Loop over equal symbols
lines.push("CheckEqual > HALT = L");                         // Final check done, halt
lines.push("CountB_0 > HALT < L");                           // No more B's, halt
lines.push("CountB_0 _ CheckEqual _ L");                     // If done counting B, move to check
lines.push("CountB_0 | CountB_0 | L");                       // Stay in same state while scanning

lines.push("INIT | CountA_1 | R");                           // Begin counting A symbols

for (let n = 1; n <= MAX_N; n++) {
    lines.push(`CountA_${n} | CountA_${n + 1} | R`);         // Count next A
    lines.push(`CountA_${n} , CountB_${n} > R`);             // Switch to counting B
    lines.push(`CountB_${n} _ HALT _ L`);                    // No more B, halt
    lines.push(`CountB_${n} | CountB_${n - 1} | R`);         // Count next B
}

const output = lines.join('\n');

const sim = new TuringMachine(output);
const play_test = 0
const init_tape  = "||||,||"
sim.run_machine(init_tape, play_test, true);

// const outputPath = path.join(__dirname, 'unary_comparison.txt');
// fs.writeFileSync(outputPath, output);

