/**
 * Marches And Gnatts - Puzzle 0
Solution Started: Jul 25, 2025
Puzzle Link: https://mng.quest/quest/tutorial
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
INIT | FIND | R
FIND | FIND | R
FIND _ HALT | R
`;

const sim = new TuringMachine(rules);
const play_test = 0
const init_tape  = "||||"
sim.run_machine(init_tape, play_test, true);

// const outputPath = path.join(__dirname, 'unary_increment.txt');
// fs.writeFileSync(outputPath, rules);

