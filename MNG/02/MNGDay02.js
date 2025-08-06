/**
 * Marches And Gnatts - Puzzle 2
Solution Started: Jul 26, 2025
Puzzle Link: https://mng.quest/quest/2/unary-even-odd
Solution by: Abbas Moosajee
Brief: [Unary Even Odd]
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

import { TuringConfig, MachineLogic } from '../TuringMachineSim/javascript_machine/TuringBrain.js';
import { TuringMachine } from '../TuringMachineSim/javascript_machine/BasicRunner.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const rules = `
INIT | ODD  _ R
ODD  | INIT _ R
ODD  _ HALT O R
INIT _ HALT E R
`;

const sim = new TuringMachine(rules);
const play_test = 0
const init_tape  = "|||||||"
sim.run_machine(init_tape, play_test, true);

// const outputPath = path.join(__dirname, 'unary_even_odd.txt');
// fs.writeFileSync(outputPath, rules);

