=begin
FlipFlop 2026: BitFlop Internship - Puzzle 11
Solution Started: August 9, 2026
Puzzle Link: https://flipflop.slome.org/2026/11
Solution by: Abbas Moosajee
Brief: [Humongous Trees]
=end

#!/usr/bin/env ruby

require 'pathname'
require 'set'

DIRECTIONS = {"L" => [0, -1], "R" => [0, 1], "T" => [1, 0]}

def parse_dna(raw_dna)
  def split_row(row, chunk_len=10, gap=2)
    step = chunk_len + gap
    (0...row.length).step(step).map do |i|
      row[i, chunk_len].split("  ")
    end
  end

  def p(token)
    token == "XX" ? nil : token
  end

  all_rules = []
  raw_dna.each_with_index do |block, line_no|
    top_row, bottom_row = block.split("\n")[0..1]
    bottom_chunks = split_row(bottom_row)
    top_chunks = split_row(top_row)

    rules = {}
    bottom_chunks.each_with_index do |bottom, stem_idx|
      parsed_stem = bottom[1].strip
      # Compare as integers to match Python behavior
      if stem_idx != parsed_stem.to_i
        raise "Parsing error on block #{line_no}: expected stem #{stem_idx}, got #{parsed_stem}"
      end
      # Use the string version as the key to match Python
      rules[parsed_stem] = [p(bottom[0]), p(top_chunks[stem_idx][2]), p(bottom[2])]  # [L, T, R]
    end
    all_rules << rules
  end
  all_rules
end

# ---------------------------------------------------------------------------
# Growth / energy mechanics
# ---------------------------------------------------------------------------
def grow(next_sprouts, blockers, y, x, child)
  return if child.nil?
  return if blockers.include?([y, x])
  key = [y, x]
  if !next_sprouts.key?(key) || next_sprouts[key] < child
    next_sprouts[key] = child
  end
end

def requested_energy(sprouts, stems)
  3 * (sprouts.length + stems.length)
end

def harvested_energy(stems, blockers, age)

  by_col = Hash.new { |h, k| h[k] = [] }
  blockers.each do |(h, x)|
    by_col[x] << h
  end

  total = 0
  stems.each do |(y, x)|
    heights = by_col[x] || []
    blocking = heights.count { |h| y < h && h <= age }
    blocking = [blocking, 3].min
    total += [y + 1, 10].min * (3 - blocking)
  end
  total
end

def solve_part1(all_rules, num_years=100)
  total = 0
  all_rules.each do |rules|
    sprouts = {[0, 0] => "00"}
    stems = Set.new

    (1..num_years).each do |age|
      next_sprouts = {}
      sprouts.each do |(y, x), sid|
        left, top, right = rules[sid]
        grow(next_sprouts, stems, y, x - 1, left)
        grow(next_sprouts, stems, y, x + 1, right)
        grow(next_sprouts, stems, y + 1, x, top)
        stems.add([y, x])  # becomes a permanent stem this year
      end

      sprouts = next_sprouts

      if age >= 5 && harvested_energy(stems, stems, age) < requested_energy(sprouts, stems)
        break
      end
    end

    total += sprouts.length + stems.length
  end
  total
end

def evolve_all(all_rules, all_sprouts, num_years=100)

  all_stems = all_rules.map { Set.new }
  all_dead = [false] * all_rules.length

  (1..num_years).each do |age|
    occupied = Set.new
    all_stems.each { |stems| occupied.merge(stems) }
    all_sprouts.each { |sprouts| occupied.merge(sprouts.keys) }

    all_rules.each_with_index do |rules, i|
      next if all_dead[i]
      
      sprouts = all_sprouts[i]
      stems = all_stems[i]
      next_sprouts = {}
      
      sprouts.each do |(y, x), sid|
        left, top, right = rules[sid]
        grow(next_sprouts, occupied, y, x - 1, left)
        grow(next_sprouts, occupied, y, x + 1, right)
        grow(next_sprouts, occupied, y + 1, x, top)
        stems.add([y, x])
      end

      sprouts.clear
      sprouts.merge!(next_sprouts)
      occupied.merge(sprouts.keys)
    end

    if age >= 5
      all_stems_flat = Set.new
      all_stems.each { |stems| all_stems_flat.merge(stems) }
      
      all_rules.each_with_index do |_, i|
        next if all_dead[i]
        sprouts = all_sprouts[i]
        stems = all_stems[i]
        if harvested_energy(stems, all_stems_flat, age) < requested_energy(sprouts, stems)
          all_dead[i] = true
        end
      end
    end
  end

  all_stems
end

def solve_part2(all_rules, num_years=100)
  all_sprouts = all_rules.map { {} }
  all_sprouts.each_with_index do |sprouts, i|
    sprouts[[0, 10 * i]] = "00"
  end

  all_stems = evolve_all(all_rules, all_sprouts, num_years)

  total_sprouts = all_sprouts.sum { |s| s.length }
  total_stems = all_stems.sum { |s| s.length }
  total_sprouts + total_stems
end

def solve_part3(all_rules, num_years=100)
  all_sprouts = all_rules.map { {} }
  all_sprouts.each_with_index do |sprouts, i|
    sprouts[[0, 10 * i]] = "00"
  end

  all_stems = evolve_all(all_rules, all_sprouts, num_years)

  2.times do
    # (tree_index, (y, x)) for every surviving sprout tip, across all trees
    entries = []
    all_sprouts.each_with_index do |sprouts, i|
      sprouts.each_key { |coord| entries << [i, coord] }
    end

    # Sort by column ascending, then height descending (tallest tip first)
    entries.sort_by! { |e| [e[1][1], -e[1][0]] }

    # Keep only the tallest surviving tip per column
    seen_cols = Set.new
    replanted = []
    entries.each do |i, (y, x)|
      if !seen_cols.include?(x)
        seen_cols.add(x)
        replanted << [i, x]
      end
    end

    all_rules = replanted.map { |i, _| all_rules[i] }
    all_sprouts = replanted.map { |_, x| {[0, x] => "00"} }
    all_stems = evolve_all(all_rules, all_sprouts, num_years)
  end

  total_sprouts = all_sprouts.sum { |s| s.length }
  total_stems = all_stems.sum { |s| s.length }
  total_sprouts + total_stems
end

input_file = "puzzle_11_input.txt"
input_path = Pathname.new(__FILE__).parent / input_file
data = File.read(input_path).split("\n\n")

all_rules = parse_dna(data)

puts "FlipFlop 2026, Puzzle 11"
puts "Part 1: #{solve_part1(all_rules)}"
puts "Part 2: #{solve_part2(all_rules)}"
puts "Part 3: #{solve_part3(all_rules)}"
