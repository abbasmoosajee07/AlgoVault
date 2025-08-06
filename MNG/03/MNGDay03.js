/**
 * Marches And Gnatts - Puzzle 3
Solution Started: Jul 27, 2025
Puzzle Link: https://mng.quest/quest/3/binary-increment
Solution by: Abbas Moosajee
Brief: [Binary Increment]
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

import { TuringConfig, MachineLogic } from '../TuringMachineSim/javascript_machine/TuringBrain.js';
import { TuringMachine } from '../TuringMachineSim/javascript_machine/BasicRunner.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const rules = `
INIT 0 INIT 0 R
INIT 1 INIT 1 R
INIT _ FIND _ L
FIND 1 FIND 0 L
FIND 0 HALT 1 R
FIND _ HALT 1 R
`;

const sim = new TuringMachine(rules);
const play_test = 0
const init_tape  = "1010"
sim.run_machine(init_tape, play_test, true);

// const outputPath = path.join(__dirname, 'unary_binary_inc.txt');
// fs.writeFileSync(outputPath, rules);


