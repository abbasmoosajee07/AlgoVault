/**
 * Marches And Gnatts - Puzzle 6
Solution Started: Aug 6, 2025
Puzzle Link: https://mng.quest/quest/6/unary-subtraction
Solution by: Abbas Moosajee
Brief: [Unary Subtraction]

 */

import { TuringConfig, MachineLogic } from '../TuringMachineSim/javascript_machine/TuringBrain.js';
import { TuringMachine } from '../TuringMachineSim/javascript_machine/BasicRunner.js';

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const MAX_N = 100;
const lines = [];
lines.push(`INIT | Count_1 _ R`);

for (let n = 1; n <= MAX_N; n++) {
    lines.push(`Count_${n} | Count_${n + 1}  _   R`);
    lines.push(`Count_${n} - Sub_${n} _   R`);

    if ((n-1) > 0) {
        lines.push(`Sub_${n} | Sub_${n - 1} _ R`);
        lines.push(`Sub_${n} _ Sub_${n - 1} | R`);
    } else {
        lines.push(`Sub_${n} _   HALT |  R`);
        lines.push(`Sub_${n} |   HALT _  R`);
    }
}

const output = lines.join('\n');

const sim = new TuringMachine(output);
const play_test = 0
const init_tape  = "|||||-||"
sim.run_machine(init_tape, play_test, true);

// const outputPath = path.join(__dirname, 'unary_subtraction.txt');
// fs.writeFileSync(outputPath, output);


