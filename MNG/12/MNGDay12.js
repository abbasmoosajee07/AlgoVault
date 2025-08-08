/**
 * Marches And Gnatts - Puzzle 12
Solution Started: Aug 7, 2025
Puzzle Link: https://mng.quest/quest/12/decimal-addition
Solution by: Abbas Moosajee
Brief: [Decimal Addition]

 * Day 12 - Year MNG
 * Author: Abbas Moosajee
 */

import { TuringConfig, MachineLogic } from '../TuringMachineSim/javascript_machine/TuringBrain.js';
import { TuringMachine } from '../TuringMachineSim/javascript_machine/BasicRunner.js';

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const all_numerals = "0123456789"

const rules = [];
const DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'];
const LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j'];
const MAX_N = 9;

// INIT rules
for (let n = 0; n <= MAX_N; n++) {
    rules.push(`INIT ${n} INIT ${n} R`);
}
rules.push(`INIT + INIT + R`);
rules.push(`INIT _ dec _ L`);

// dec rules
rules.push(`dec 0 shift _ L`);
for (let n = 1; n <= MAX_N; n++) {
    rules.push(`dec ${n} clean ${n-1} L`);
}
rules.push(`dec + clean _ L`);
rules.push(`clean + inc + L`);

// shift rules
for (let n = 0; n <= MAX_N; n++) {
    rules.push(`shift ${n} shift ${n} L`);
}
rules.push(`shift + fix + L`);
LETTERS.forEach(letter => {
    rules.push(`shift ${letter} fix ${letter} L`);
});

// fix rules
LETTERS.forEach(letter => {
    rules.push(`fix ${letter} fix ${letter} L`);
});
for (let n = 0; n <= MAX_N; n++) {
    rules.push(`fix ${n} INIT ${String.fromCharCode(97+n)} R`);
}
rules.push(`fix _ INIT a R`);

// inc rules
LETTERS.forEach(letter => {
    rules.push(`inc ${letter} inc ${letter} L`);
});
for (let n = 0; n < MAX_N; n++) {
    rules.push(`inc ${n} INIT ${n+1} R`);
}
rules.push(`inc 9 inc 0 L`);
rules.push(`inc _ INIT 1 R`);

// repeat rules
LETTERS.forEach(letter => {
    rules.push(`INIT ${letter} INIT ${letter} R`);
});

// clean rules
for (let n = 0; n <= MAX_N; n++) {
    rules.push(`clean ${LETTERS[n]} clean ${n} L`);
    rules.push(`clean ${n} clean ${n} L`);
}
rules.push(`clean _ HALT _ R`);

// Output the rules
const output = rules.join('\n');

// const sim = new TuringMachine(output);
// const play_test = 0
// const init_tape  = "2+5"
// sim.run_machine(init_tape, play_test, true);

const outputPath = path.join(__dirname, 'decimal_addition.txt');
fs.writeFileSync(outputPath, output);

