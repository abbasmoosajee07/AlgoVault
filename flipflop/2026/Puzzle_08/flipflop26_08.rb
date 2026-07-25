=begin
FlipFlop 2026: BitFlop Internship - Puzzle 8
Solution Started: July 26, 2026
Puzzle Link: https://flipflop.slome.org/2026/8
Solution by: Abbas Moosajee
Brief: [The Amazing Digital Stoats]
=end

#!/usr/bin/env ruby

require 'pathname'

# Define file name and extract complete path to the input file
input_file = "puzzle_08_input.txt"
input_file_path = Pathname.new(__FILE__).dirname + input_file

# Read the input data
input_data = File.readlines(input_file_path).map(&:strip)

class DigitalStoats
    def initialize(rules)
        @rules = rules
    end

    def basic_evolution(total_gens, base = 'AB')
        rules_dict = Hash.new { |h, k| h[k] = [] }
        @rules.each do |rule_str|
        stripped_rule = rule_str.delete(' ')
        rules_dict[stripped_rule[0]] << stripped_rule[1..]
        end

        (1..total_gens).each do |_gen_no|
            next_gen = +''
            base.each_char { |parent| next_gen << rules_dict[parent][0] }
            base = next_gen
        end
        base.length
    end

    def two_stoat_evolution(total_gens, base = 'AB')
        rules_dict = Hash.new { |h, k| h[k] = [] }
        @rules.each do |rule_str|
        stripped_rule = rule_str.delete(' ')
        key = stripped_rule[0, 2]
        value = stripped_rule[2..]
        rules_dict[key] << value
        rules_dict[key.reverse] << value
        end

        transition = {}
        rules_dict.each do |key, values|
        value = values[0]
        seq = key[0] + value + key[1]
        transition[key] = seq.chars.each_cons(2).map { |x, y| x + y }
        end

        # Initialize pair counts from the starting base string.
        pair_counts = Hash.new(0)
        base.chars.each_cons(2) { |a, b| pair_counts[a + b] += 1 }

        (1..total_gens).each do |gen_no|
            next_counts = Hash.new(0)
            pair_counts.each do |pair, count|
                transition[pair].each { |new_pair| next_counts[new_pair] += count }
        end
        pair_counts = next_counts
        #   puts "Gen #{gen_no}: #{pair_counts.values.sum + 1} in length"
        end

        pair_counts.values.sum + 1
    end
end

stoats = DigitalStoats.new(input_data)
puts 'FlipFlop 2026, Puzzle 08'
puts "Part 1: #{stoats.basic_evolution(7)}"
puts "Part 2: #{stoats.two_stoat_evolution(7)}"
puts "Part 2: #{stoats.two_stoat_evolution(21)}"