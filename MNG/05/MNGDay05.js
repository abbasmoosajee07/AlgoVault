/**
 * Marches And Gnatts - Puzzle 5
Solution Started: Aug 6, 2025
Puzzle Link: https://mng.quest/quest/5/find-element-in-unary-array
Solution by: Abbas Moosajee
Brief: [Find Element in Unary Array]

 * Day 05 - Year MNG
 * Author: Abbas Moosajee
 */

import { TuringConfig, MachineLogic } from '../TuringMachineSim/javascript_machine/TuringBrain.js';
import { TuringMachine } from '../TuringMachineSim/javascript_machine/BasicRunner.js';

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const MAX_N = 44;
const lines = [];
lines.push(`INIT | Count_1 _ R`);

// Check elements or traverse until you find `:` marker
for (let n = 1; n <= MAX_N; n++) {
    lines.push(`Count_${n} | Count_${n + 1}  _   R`);               // skip unary bars
    lines.push(`Count_${n} : Find_${n}     _   R`);             // found target
    lines.push(`Find_${n}  _ HALT  _   R`);

    if (n === 1) {
        lines.push(`Find_${n} | Find_${n} | R`);
    } else {
        lines.push(`Find_${n} | Find_${n} _ R`);
    }

    if (n - 1 === 0){
        lines.push(`Find_${n} , ERASE_ALL _ R`);
    } else{
        lines.push(`Find_${n} , Find_${n-1}  _ R`);
    }
}

// Cleanup: ERASE_ALL wipes everything to the right
lines.push(`ERASE_ALL |   ERASE_ALL  _   R`);
lines.push(`ERASE_ALL ,   ERASE_ALL  _   R`);
lines.push(`ERASE_ALL _   HALT       _   R`);

const output = lines.join('\n');


const sim = new TuringMachine(output);
const play_test = 0
const init_tape  = "||:|||,|||||,||||||||,||||"
sim.run_machine(init_tape, play_test, true);

// const outputPath = path.join(__dirname, 'unary_array.txt');
// fs.writeFileSync(outputPath, output);
