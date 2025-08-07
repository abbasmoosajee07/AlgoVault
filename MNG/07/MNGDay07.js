/**
 * Marches And Gnatts - Puzzle 7
Solution Started: Aug 7, 2025
Puzzle Link: https://mng.quest/quest/7/letter-mark
Solution by: Abbas Moosajee
Brief: [Letter Mark]

 * Day 07 - Year MNG
 * Author: Abbas Moosajee
 */


import { TuringConfig, MachineLogic } from '../TuringMachineSim/javascript_machine/TuringBrain.js';
import { TuringMachine } from '../TuringMachineSim/javascript_machine/BasicRunner.js';

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const valid_letters = "abcdefghijklmnopqrstuvwxyzäöõü-";
const extra_symbols = "[]:";
const lines = ["// wõta-wastu-mu-soow-ja-chillitse-toomemäel"];

lines.push("MARK_w _ MARK_w1 [ R");
lines.push("MARK_w1 _ MARK_w2 w R");
lines.push("MARK_w2 _ GO_START ] L");
lines.push("GO_START _ START _ R");
lines.push("MARK_ch h MARK_ch _ R");
lines.push("MARK_ch _ MARK_ch1 [ R");
lines.push("MARK_ch1 _ MARK_ch2 c R");
lines.push("MARK_ch2 _ MARK_ch3 h R");
lines.push("MARK_ch3 _ GO_START ] L");
lines.push("START : HALT _ R");
lines.push("INIT _ GO_START : L");

// INIT state transitions
for (const char of valid_letters) {
    lines.push(`INIT ${char} INIT ${char} R`);

    if (char === "w") {
        lines.push("START w MARK_w _ R");
    } else if (char === "c") {
        lines.push("START c MARK_ch _ R");
    } else {
        lines.push(`START ${char} COPY_${char} _ R`);

        for (const copy_char of valid_letters + extra_symbols) {
            lines.push(`COPY_${char} ${copy_char} COPY_${char} ${copy_char} R`);
        }
        lines.push(`COPY_${char} _ GO_START ${char} L`);
    }
}

for (const extra_char of valid_letters + extra_symbols) {
    lines.push(`GO_START ${extra_char} GO_START ${extra_char} L`);
    lines.push(`MARK_w ${extra_char} MARK_w ${extra_char} R`);
    if (extra_char !== "h") {
        lines.push(`MARK_ch ${extra_char} MARK_ch ${extra_char} R`);
    }
}

const output = lines.join('\n');


const sim = new TuringMachine(output);
const play_test = 0
const START_tape  = "wõta-wastu-mu-soow-ja-chillitse-toomemäel"
sim.run_machine(START_tape, play_test, true);

// const outputPath = path.join(__dirname, 'letter_mark.txt');
// fs.writeFileSync(outputPath, output);


