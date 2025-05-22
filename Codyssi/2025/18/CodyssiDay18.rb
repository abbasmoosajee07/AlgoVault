=begin
Codyssi Puzzles - Problem 18
Solution Started: May 20, 2025
Puzzle Link: https://www.codyssi.com/view_problem_22?
Solution by: Abbas Moosajee
Brief: [Code/Problem Description]
=end

#!/usr/bin/env ruby

require 'pathname'
require 'time'
require 'matrix'
start_time = Time.now

# Define file name and extract complete path to the input file
D18_file = "Day18_input.txt"
D18_file_path = Pathname.new(__FILE__).dirname + D18_file

input_data = File.read(D18_file_path).strip.split("\n")

data = File.readlines(D18_file_path, chomp: true)
feasible, target_coords = [[10, 15, 60, 3], [9, 14, 59, 0]]

DIM_X, DIM_Y, DIM_Z, DIM_A = feasible
DIM_XYZA = DIM_X * DIM_Y * DIM_Z * DIM_A
DIM_YZA = DIM_Y * DIM_Z * DIM_A
DIM_ZA = DIM_Z * DIM_A
DEBRIS_CYCLE = DIM_X.lcm(DIM_Y).lcm(DIM_Z).lcm(DIM_A)
MAX_SAFE_HITS = 3

def idx(x, y, z, a)
  x * DIM_YZA + y * DIM_ZA + z * DIM_A + a + 1
end

def idxr(pos)
  x, rem = pos.divmod(DIM_YZA)
  y, rem = rem.divmod(DIM_ZA)
  z, rem = rem.divmod(DIM_A)
  a = rem - 1
  [x, y, z, a]
end

debris = Array.new(DEBRIS_CYCLE) { Array.new(DIM_XYZA, 0) }

data.each do |line|
  s = line.split
  ss = s[2].split("+")
  fx = ss[0][..-2].to_i
  fy = ss[1][..-2].to_i
  fz = ss[2][..-2].to_i
  fa = ss[3][..-2].to_i
  d = s[4].to_i
  r = s[7].to_i
  vx = s[11][1..-2].to_i
  vy = s[12][0..-2].to_i
  vz = s[13][0..-2].to_i
  va = s[14][0..-2].to_i

  (0...DIM_XYZA).each do |pos|
    x, y, z, a = idxr(pos)
    if (fx * x + fy * y + fz * z + fa * a) % d == r
      debris[0][idx(x, y, z, a)] += 1
      (1...DEBRIS_CYCLE).each do |t|
        x = (x + vx) % DIM_X
        y = (y + vy) % DIM_Y
        z = (z + vz) % DIM_Z
        a = (a + va + 1) % DIM_A - 1
        debris[t][idx(x, y, z, a)] += 1
      end
    end
  end
end

ans1 = debris[0].sum
puts "Part 1: #{ans1}"

start = idx(0, 0, 0, 0)
target = idx(target_coords[0], target_coords[1], target_coords[2], target_coords[3])
safe = Array.new(DIM_XYZA, false)
safe[start] = true

t = 0
until safe[target]
  t += 1
  safe_new = safe.dup
  safe.each_with_index do |ok, pos|
    next unless ok
    x, y, z, a = idxr(pos)
    safe_new[idx(x - 1, y, z, a)] = true if x > 0
    safe_new[idx(x + 1, y, z, a)] = true if x < DIM_X - 1
    safe_new[idx(x, y - 1, z, a)] = true if y > 0
    safe_new[idx(x, y + 1, z, a)] = true if y < DIM_Y - 1
    safe_new[idx(x, y, z - 1, a)] = true if z > 0
    safe_new[idx(x, y, z + 1, a)] = true if z < DIM_Z - 1
  end
  safe = safe_new
  debris[t % DEBRIS_CYCLE].each_with_index do |count, pos|
    safe[pos] = false if count > 0
  end
  safe[start] = true
end

ans2 = t
puts "Part 2: #{ans2}"

hits = Array.new(DIM_XYZA, MAX_SAFE_HITS + 1)
hits[start] = 0

t = 0
while hits[target] > MAX_SAFE_HITS
  t += 1
  hits_new = hits.dup
  hits.each_with_index do |hit_count, pos|
    next if hit_count > MAX_SAFE_HITS
    x, y, z, a = idxr(pos)
    [[-1, 0], [1, 0]].each do |dx, _|
      nx = x + dx
      hits_new[idx(nx, y, z, a)] = [hits_new[idx(nx, y, z, a)], hit_count].min if (0...DIM_X).include?(nx)
    end
    [[-1, 0], [1, 0]].each do |dy, _|
      ny = y + dy
      hits_new[idx(x, ny, z, a)] = [hits_new[idx(x, ny, z, a)], hit_count].min if (0...DIM_Y).include?(ny)
    end
    [[-1, 0], [1, 0]].each do |dz, _|
      nz = z + dz
      hits_new[idx(x, y, nz, a)] = [hits_new[idx(x, y, nz, a)], hit_count].min if (0...DIM_Z).include?(nz)
    end
  end
  hits = hits_new
  debris[t % DEBRIS_CYCLE].each_with_index do |count, pos|
    hits[pos] += count
  end
  hits[start] = 0
end

ans3 = t
puts "Part 3: #{ans3}"

# puts "Execution Time = #{Time.now - start_time}s"
