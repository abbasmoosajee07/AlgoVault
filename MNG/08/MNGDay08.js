/**
* Marches And Gnatts - Puzzle 8
Solution Started: Aug 7, 2025
Puzzle Link: https://mng.quest/quest/8/text-mirror
Solution by: Abbas Moosajee
Brief: [Text Mirror]
*/


import { TuringConfig, MachineLogic } from '../TuringMachineSim/javascript_machine/TuringBrain.js';
import { TuringMachine } from '../TuringMachineSim/javascript_machine/BasicRunner.js';

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const lines = ["// hello-world"];
const valid_letters = "abcdefghijklmnopqrstuvwxyzäöõü-"
const extra_symbols = ":.";

lines.push("INIT  _ MOVE_L : L");
lines.push("IGNORE : MOVE_L : L");
lines.push("MOVE_L . MOVE_L . L");
lines.push("MOVE_L _ Final _ R");
lines.push("Final . Final _ R");
lines.push("Final : HALT _ R");

for (const char of valid_letters) {
    lines.push(`INIT ${char} INIT ${char} R`);
    lines.push(`MOVE_L ${char} COPY_${char} . R`);

    lines.push(`COPY_${char} _ IGNORE ${char} L`);
    lines.push(`IGNORE ${char} IGNORE ${char} L`);

    for (const ig_char of valid_letters + extra_symbols) {
        lines.push(`COPY_${char} ${ig_char}  COPY_${char} ${ig_char} R`)
    }
}
const output = lines.join('\n');

const sim = new TuringMachine(output);
const play_test = 0
const init_tape  = "hello-world"
sim.run_machine(init_tape, play_test, true);

// const outputPath = path.join(__dirname, 'text_mirror.txt');
// fs.writeFileSync(outputPath, output);
