
import { MNG_ARENA } from '../MNG_ARENA.js';

const unary_mult_rules = `
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


const unary_mult = new MNG_ARENA("Quest04_input")
unary_mult.full_solution(unary_mult_rules);
unary_mult.benchmark_solution(["||*|||", "||||*|||", "||||||||*|||"], false)
// unary_mult.test_solution("||*|||", true)
// unary_mult.save_rules(import.meta.url);
