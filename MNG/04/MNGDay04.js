import { TuringConfig, MachineLogic } from '../TuringMachineSim/javascript_machine/TuringBrain.js';
import { TuringMachine } from '../TuringMachineSim/javascript_machine/BasicRunner.js';


// Example usage:
const rules = `
INIT  | toB   _ R   // Erase | from a, move to copy b
INIT  * SKIP  _ R   // All of a consumed, erase '*' and move to HALT

toB   | toB   | R
toB   * eachB * R   // Move to start copying b

nextA _ INIT  _ R   // After one copy of b, move back to INIT
nextA | nextA | L
nextA * nextA * L

SKIP  | SKIP  _ R   // Erase b
SKIP  _ HALT  _ R

eachB _ nextA _ L   // No more b to copy
eachB | sep   _ R   // Copy this '|', erase original

sep   _ add   _ R
sep   | sep   | R

add   _ sepL  | L   // Add copy of b to end
add   | add   | R

sepL  _ nextB _ L
sepL  | sepL  | L

nextB _ eachB | R   // Go back to copy next '|'
nextB | nextB | L
`;
// console.log("HELLO");

const sim = new TuringMachine(rules);
const play_test = 0
const init_tape = "|||*|||"
sim.run_machine(init_tape, play_test, false);

