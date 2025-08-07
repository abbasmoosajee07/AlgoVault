/**
 * Marches And Gnatts - Puzzle 11
Solution Started: Aug 7, 2025
Puzzle Link: https://mng.quest/quest/11/decimal-increment
Solution by: Abbas Moosajee
Brief: [Decimal Increment]

 * Day 11 - Year MNG
 * Author: Abbas Moosajee
 */

import { TuringConfig, MachineLogic } from '../TuringMachineSim/javascript_machine/TuringBrain.js';
import { TuringMachine } from '../TuringMachineSim/javascript_machine/BasicRunner.js';

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const output = `// Decimal Increment
INIT 0 INIT 0 R
INIT 1 INIT 1 R
INIT 2 INIT 2 R
INIT 3 INIT 3 R
INIT 4 INIT 4 R
INIT 5 INIT 5 R
INIT 6 INIT 6 R
INIT 7 INIT 7 R
INIT 8 INIT 8 R
INIT 9 INIT 9 R
INIT _ NUM  _ L

NUM  0 HALT 1 R
NUM  1 HALT 2 R
NUM  2 HALT 3 R
NUM  3 HALT 4 R
NUM  4 HALT 5 R
NUM  5 HALT 6 R
NUM  6 HALT 7 R
NUM  7 HALT 8 R
NUM  8 HALT 9 R
NUM  9 NUM  0 L
NUM  _ HALT 1 R
`

const sim = new TuringMachine(output);
const play_test = 0
const init_tape  = "13"
sim.run_machine(init_tape, play_test, true);

const outputPath = path.join(__dirname, 'decimal_increment.txt');
fs.writeFileSync(outputPath, output);

