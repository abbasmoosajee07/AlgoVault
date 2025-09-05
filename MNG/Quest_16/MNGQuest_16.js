/* Marches And Gnatts - Quest 16
Solution Started: September 5, 2025
Puzzle Link: https://mng.quest/quest/16/
Solution by: Abbas Moosajee
Brief: [Roman unary]
*/

import { MNG_ARENA } from '../MNG_ARENA.js';

const NUMERALS = [
    ["I", 1],
    ["V", 5],
    ["X", 10],
    ["L", 50],
    ["C", 100],
    ["D", 500],
    ["M", 1000]
];

const NUMERAL_SYMBOLS = new Set(NUMERALS.map(([sym, _]) => sym));

const IGNORING = {
    1: new Set(["I"]),
    5: new Set(["I"]),
    10: new Set(["I","V","X"]),
    40: new Set(["I","V","X"]),
    50: new Set(["I","V","X"]),
    90: new Set(["I","V","X"]),
    100: new Set(["I","V","X","L","C"]),
    400: new Set(["I","V","X","L","C"]),
    500: new Set(["I","V","X","L","C"]),
    900: new Set(["I","V","X","L","C"]),
    1000: new Set(["I","V","X","L","C","D","M"])
};

const CAN_SUBTRACT = {
    "I": new Set(["V","X"]),
    "X": new Set(["L","C"]),
    "C": new Set(["D","M"])
};

function romanUnary(turingMachine) {
    let seenValues = new Set();

    // Initial rules: convert each numeral to its value
    for (const [sym, value] of NUMERALS) {
        turingMachine.add_rule("INIT", sym, `ADD_${value}`, "_", "R");
        seenValues.add(value);

        for (const [largerSym, largerValue] of NUMERALS) {
            if (!CAN_SUBTRACT[sym] || !CAN_SUBTRACT[sym].has(largerSym)) continue;
            turingMachine.add_rule(`ADD_${value}`, largerSym, `ADD_${largerValue - value}`, "_", "R");
            seenValues.add(largerValue - value);
        }
    }

    // Add rules for decreasing values
    for (const value of seenValues) {
        const ignoreSet = new Set(["|"]);
        if (IGNORING[value]) {
            for (const s of IGNORING[value]) ignoreSet.add(s);
        }
        const nextState = (value !== 1) ? `ADD_${value-1}` : "NEXT";
        const direction = (value !== 1) ? "R" : "L";
        turingMachine.find_state(`ADD_${value}`, "_", ignoreSet, "R", nextState, "|", direction);
    }

    // Fill in missing values
    for (let value = 1; value < Math.max(...seenValues); value++) {
        if (seenValues.has(value)) continue;
        const nextState = (value !== 1) ? `ADD_${value-1}` : "NEXT";
        turingMachine.add_rule(`ADD_${value}`, "_", nextState, "|", "R");
    }

    // Go to next numeral
    turingMachine.find_state("NEXT", "_", new Set([...NUMERAL_SYMBOLS, "|"]), "L", "INIT", "_", "R");

    // Halt when input consumed
    for (const [sym, value] of NUMERALS) {

        turingMachine.add_rule("FINISH", sym, `FINISH`, "_", "R");
    }
    turingMachine.add_rule("FINISH", "|", "HALT", "|", "L");
    turingMachine.add_rule("FINISH", "_", "HALT", "_", "R");
    turingMachine.add_rule("INIT", "|", "FINISH", "|", "R");
}

// Example usage:
const romanUnaryMachine = new MNG_ARENA("Quest16_input");
romanUnary(romanUnaryMachine);

// Test case
const testTape = "IX";
romanUnaryMachine.benchmark_solution([testTape, "XIV", "CX"], false)

// romanUnaryMachine.test_solution(testTape, false);
romanUnaryMachine.save_rules(import.meta.url);