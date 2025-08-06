/**
 * Marches And Gnatts - Puzzle 1
Puzzle Link: https://mng.quest/quest/1/unary-addition
Solution by: Abbas Moosajee
Brief: [Unary Addition]
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

import { TuringConfig, MachineLogic } from '../TuringMachineSim/javascript_machine/TuringBrain.js';
import { TuringMachine } from '../TuringMachineSim/javascript_machine/BasicRunner.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const rules = `
INIT | FIND _ R
FIND | FIND | R
FIND + HALT | R
`;

const sim = new TuringMachine(rules);
const play_test = 0
const init_tape  = "|||+||||"
sim.run_machine(init_tape, play_test, true);

// const outputPath = path.join(__dirname, 'unary_addition.txt');
// fs.writeFileSync(outputPath, rules);
