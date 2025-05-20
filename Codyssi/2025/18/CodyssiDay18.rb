=begin
Codyssi Puzzles - Problem 18
Solution Started: May 20, 2025
Puzzle Link: https://www.codyssi.com/view_problem_22?
Solution by: Abbas Moosajee
Brief: [Code/Problem Description]
=end

#!/usr/bin/env ruby

require 'pathname'
require 'set'
require 'time'
require 'algorithms'

# Define file name and extract complete path to the input file
D18_file = "Day18_input.txt"
D18_file_path = Pathname.new(__FILE__).dirname + D18_file

start_time = Time.now

input_data = File.read(D18_file_path).strip.split("\n")

feasible_spaces = {
  "Day18_input1.txt" => [[10, 15, 60, 3], [9, 14, 59, 0]],
  "Day18_input2.txt" => [[3, 3, 5, 3], [2, 2, 4, 0]],
  "Day18_input.txt" => [[10, 15, 60, 3], [9, 14, 59, 0]],
  "Day18_input3.txt" => [[10, 15, 60, 3], [9, 14, 59, 0]]
}

feasible, target_coords = feasible_spaces[D18_file]

class Submarine
  attr_reader :debris_map

  def initialize(all_rules, feasible_space)
    @idx_map = {"x" => 0, "y" => 1, "z" => 2, "a" => 3}
    @rule_dict = {}
    all_rules.each { |rule| parse_rules(rule) }

    min_limits = [0, 0, 0, -1]
    @space_region = {
      "x" => (min_limits[0]...feasible_space[0]),
      "y" => (min_limits[1]...feasible_space[1]),
      "z" => (min_limits[2]...feasible_space[2]),
      "a" => (min_limits[3]...feasible_space[3] - 1)
    }

    @all_coords = @space_region["x"].to_a.product(
      @space_region["y"].to_a,
      @space_region["z"].to_a,
      @space_region["a"].to_a
    )
  end

  def parse_rules(rule)
    rule_no_str, info = rule.split(": ", 2)
    rule_no = rule_no_str.gsub("RULE ", "").to_i
    pattern = /(\d+)x\+(\d+)y\+(\d+)z\+(\d+)a DIVIDE (\d+) HAS REMAINDER (\d+) \| DEBRIS VELOCITY \((-?\d+), (-?\d+), (-?\d+), (-?\d+)\)/

    match = pattern.match(info)
    values = match.captures.map(&:to_i)

    @rule_dict[rule_no] = {
      "x" => values[0], "y" => values[1], "z" => values[2], "a" => values[3],
      "div" => values[4], "rem" => values[5],
      "vx" => values[6], "vy" => values[7], "vz" => values[8], "va" => values[9]
    }
  end

  def check_debris(coords, rule_no)
    rule = @rule_dict[rule_no]
    total = rule["x"] * coords[0] + rule["y"] * coords[1] + rule["z"] * coords[2] + rule["a"] * coords[3]
    total % rule["div"] == rule["rem"]
  end

  def count_debris
    @debris_map = []
    @all_coords.each do |coords|
      @rule_dict.each_key do |rule_no|
        @debris_map << [rule_no, coords] if check_debris(coords, rule_no)
      end
    end
    @debris_map.length
  end

  def wrapped_move(pos, delta, dim, wrapping)
    min_val = @space_region[dim].min
    max_val = @space_region[dim].max
    range_size = @space_region[dim].size
    new_pos = pos + delta

    if wrapping
      (new_pos - min_val) % range_size + min_val
    elsif new_pos.between?(min_val, max_val)
      new_pos
    else
      pos
    end
  end

  def move_particle(rule, particle, time = 1, wrapping = true)
    new_coords = []
    @idx_map.each do |dim, idx|
      velocity = @rule_dict[rule]["v#{dim}"]
      delta = velocity * time
      new_coords[idx] = wrapped_move(particle[idx], delta, dim, wrapping)
    end
    new_coords
  end

  def move_in_dimension(coords, move, time = 1, wrapping = false)
    dim, velocity = move
    idx = @idx_map[dim]
    delta = velocity * time
    new_coords = coords.dup
    new_coords[idx] = wrapped_move(coords[idx], delta, dim, wrapping)
    new_coords
  end

  def find_flight_path(target, start = [0, 0, 0, 0])
    all_moves = ["x", "y", "z"].product([1, -1, 0])
    position_history = {0 => @debris_map.dup}
    min_time = Float::INFINITY
    queue = [[start, 0]]
    visited = Set.new
    count = 0

    until queue.empty?
      current_pos, time_step = queue.shift
      count += 1

      if current_pos == target
        min_time = [min_time, time_step].min
        next
      end

      next if time_step > min_time || visited.include?([current_pos, time_step])
      visited.add([current_pos, time_step])

      next_time = time_step + 1
      occupied = position_history[next_time] || Set.new(@debris_map.map { |rule, pos| move_particle(rule, pos, next_time) })
      position_history[next_time] ||= occupied

      all_moves.each do |move|
        next_pos = move_in_dimension(current_pos, move)
        if !occupied.include?(next_pos) || next_pos == start
          queue << [next_pos, next_time]
        end
      end
    end

    min_time
  end
end

sub = Submarine.new(input_data, feasible)

debris = sub.count_debris
puts "Part 1: #{debris}"

flight_time = sub.find_flight_path(target_coords)
puts "Part 2: #{flight_time}"

# puts "Execution Time = #{Time.now - start_time}s"
