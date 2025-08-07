/**
 * Marches And Gnatts - Puzzle 10
Solution Started: Aug 7, 2025
Puzzle Link: https://mng.quest/quest/10/
Solution by: Abbas Moosajee
Brief: [Code/Problem Description]

 * Day 10 - Year MNG
 * Author: Abbas Moosajee
 */
import { TuringConfig, MachineLogic } from '../TuringMachineSim/javascript_machine/TuringBrain.js';
import { TuringMachine } from '../TuringMachineSim/javascript_machine/BasicRunner.js';

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const all_letters = "abcdefghijklmnopqrstuvwxyzäöõü-"

const fewest_steps = [];
const fewest_rules = [];

for (const char of all_letters) {
    fewest_steps.push(`INIT ${char} INIT . R`);
    fewest_rules.push(`INIT ${char} INIT _ R`);
    fewest_rules.push(`INC ${char} INC ${char} R`);
    fewest_rules.push(`RETURN ${char} RETURN ${char} L`);
}

fewest_steps.push(`INIT + INIT | R`);
fewest_steps.push(`INIT _ Count_1 _ L`);

const MAX_N = 699;
for (let n = 1; n <= MAX_N; n++) {
    fewest_steps.push(`Count_${n} . Count_${n} _ L`)
    fewest_steps.push(`Count_${n} | Count_${n + 1} _ L`)
    if (n === 1) {
        fewest_steps.push(`Count_${n} _ HALT | L`)
    } else {
        fewest_steps.push(`Count_${n} _ Count_${n - 1} | L`)
    }

}

// Core transitions
fewest_rules.push(`INC + INC + R`);
fewest_rules.push(`RETURN + RETURN + L`);
fewest_rules.push("INC | INC | R");
fewest_rules.push("RETURN | RETURN | L");
fewest_rules.push("FINISH | FINISH | R");
fewest_rules.push("INIT   + INC    _ R");
fewest_rules.push("INC    _ RETURN | L");
fewest_rules.push("RETURN _ INIT   _ R");
fewest_rules.push("INIT   | FINISH | R");
fewest_rules.push("INIT   _ HALT   | R");
fewest_rules.push("FINISH _ HALT   | R");


const output = fewest_steps.join('\n');

const sim = new TuringMachine(output);
const play_test = 0
const init_tape  = "hello+world+how-are-you"
sim.run_machine(init_tape, play_test, true);

// const outputPath = path.join(__dirname, 'lines_count.txt');
// fs.writeFileSync(outputPath, output);

