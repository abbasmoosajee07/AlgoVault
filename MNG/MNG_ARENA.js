import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

import { TuringConfig, MachineLogic } from './TuringMachineSim/javascript_machine/TuringBrain.js';
import { TuringMachine } from './TuringMachineSim/javascript_machine/BasicRunner.js';


class MNG_ARENA {
    constructor(quest_name) {
        this.quest_name = quest_name;
        this.rules = [];
    }

    full_solution(rules_set){
        this.rules = rules_set.split("\n");
    }

    add_comment(comment_line) {
        this.rules.push(`// ${comment_line}`);
    }

    validate_rule(parts) {
        if (parts.length !== 5) {
            throw new Error(`Invalid rule format: expected 5 parts, got ${parts.length} → "${parts.join(" ")}"`);
        }
    }

    add_rule(state, symbol, newState, newSymbol, dir) {
        const parts = [state, symbol, newState, newSymbol, dir].map(String);
        this.validate_rule(parts);
        this.rules.push(parts.join(" "));
    }

    ignore(state, symbol, dir) {
        const parts = [state, symbol, state, symbol, dir].map(String);
        this.validate_rule(parts);
        this.rules.push(parts.join(" "));
    }

    find_state(fromState, needle, ignoring, searchDir, toState, toSymbol, toDir = null) {
        // Ignore given symbols while moving in searchDir
        for (let ignore_sym of ignoring){
            this.ignore(fromState, ignore_sym, searchDir);
        }

        // Default direction: opposite of searchDir
        const moveDir = toDir !== null ? toDir : (searchDir === "L" ? "R" : "R");

        if (needle instanceof Set) {
            for (let n of needle) {
                this.add_rule(fromState, n, toState, toSymbol, moveDir);
            }
        } else {
            this.add_rule(fromState, needle, toState, toSymbol, moveDir);
        }
    }

    test_solution(test_tape, visualize = true) {
        if (this.rules.length === 0) {
            throw new Error("No rules have been defined. Cannot run test_solution.");
        }
        const rules_set = this.rules.join("\n");
        const sim = new TuringMachine(rules_set);
        sim.run_machine(test_tape, 0, visualize);
    }

    benchmark_solution(tape_list, visualize = false) {
        if (!Array.isArray(tape_list) || tape_list.length === 0) {
            throw new Error("tape_list must be a non-empty array of tape strings.");
        }
        if (this.rules.length === 0) {
            throw new Error("No rules have been defined. Cannot run benchmark.");
        }

        const rules_set = this.rules.join("\n");
        let total_steps = 0;

        tape_list.forEach((tape, index) => {
            const tape_sim = new TuringMachine(rules_set);
            tape_sim.run_machine(tape, 0, visualize);

            const tape_steps = tape_sim.step_count || 0;
            console.log(`Tape #${index + 1}: '${tape}' -> '${tape_sim.cpu._printTapeState(false)}'  (${tape_steps} steps)`);

            total_steps += tape_steps;
        });

        console.log(`Quest ${this.quest_name} | Total Steps: ${total_steps}`);
        return total_steps;
    }

    save_rules(storeLoc = process.cwd()) {
        const file_name = `${this.quest_name}.txt`;
        const rules_set = this.rules.join("\n");

        try {
            const __filename = fileURLToPath(storeLoc);
            const __dirname = path.dirname(__filename);
            const outputPath = path.join(__dirname, file_name);
            fs.writeFileSync(outputPath, rules_set, 'utf-8');
            console.log(`Rules saved to: ${outputPath}`);
        } catch (err) {
            console.error(`Failed to save rules: ${err.message}`);
            throw err;
        }
    }
}

export {MNG_ARENA}