# Python file for solving the puzzles of day 16 of Advent of Code 2023
import itertools as it
import numpy as np
import sys
import re

def parse(puzzle_input):
	'''Method for parsing the puzzle input into a more suitable format for computations'''
	with open(puzzle_input, 'r+') as f:
		parsed_input = np.array([[x for x in line.strip()] for line in f.readlines()])
	return parsed_input

def part1(parsed_input, start_direction, start_y, start_x):
	nrows, ncols = parsed_input.shape
	direction_increments = {0: (0, -1), 1: (-1,0), 2: (0,1), 3: (1, 0)} # 0: left, 1: up, 2: right, 3: down
	direction_switches = {
		'/': {i: 3 - i for i in range(4)},
		'\\': {0: 1, 1: 0, 2: 3, 3: 2},
	}
	visited_combos = set() # combinations of (tile, direction), to prune when already visited to avoid cycles
	beams = {0: {'direction': start_direction, 'y': start_y, 'x': start_x}}
	idx = 1

	# Process starting position
	symbol = parsed_input[start_y, start_x] 
	if symbol in ['\\', '/']:
		beams[0]['direction'] = direction_switches[symbol][start_direction]
	elif (symbol == '|' and start_direction % 2 == 0) or (symbol == '-' and start_direction % 2 == 1):
		beams[idx] = {'direction': (start_direction - 1) % 4, 'y': start_y, 'x': start_x}
		beams[idx+1] = {'direction': (start_direction + 1) % 4, 'y': start_y, 'x': start_x}
		idx += 2

		del beams[0]

	while len(beams):
		beam_ids = list(beams.keys())
		for beam_id in beam_ids:
			combo = tuple(beams[beam_id].values())
			if combo in visited_combos:
				# We have completed a cycle
				del beams[beam_id]
				continue
			visited_combos.add(combo)

			# Process the beam
			direction, y, x = combo
			dy, dx = direction_increments[direction]
			new_y = y + dy
			new_x = x + dx

			if new_y not in range(nrows) or new_x not in range(ncols):
				# Beam gets out of bounds, so prune
				del beams[beam_id]
				continue
			else:
				if parsed_input[new_y][new_x] == '.' or \
					(direction % 2 == 0 and parsed_input[new_y][new_x] == '-') or \
					(direction % 2 == 1 and parsed_input[new_y][new_x] == '|'):
					# Empty tile or pointy end of splitter; just move in the direction
					beams[beam_id]['y'] = new_y
					beams[beam_id]['x'] = new_x
				
				elif parsed_input[new_y][new_x] in ['/', '\\']:
					# Mirror; determine new direction
					beams[beam_id]['direction'] = direction_switches[parsed_input[new_y][new_x]][direction]
					beams[beam_id]['y'] = new_y
					beams[beam_id]['x'] = new_x
					
				else:
					# Flat part of splitter: split into two new beams
					beams[idx] = {'direction': (direction - 1) % 4, 'y': new_y, 'x': new_x}
					beams[idx + 1] = {'direction': (direction + 1) % 4, 'y': new_y, 'x': new_x}
					del beams[beam_id]
					idx += 2

	return len(set((y,x) for (d,y,x) in visited_combos))			




def part2(parsed_input):
	nrows, ncols = parsed_input.shape
	max_score = 0
	
	# Left axis
	for r in range(nrows):
		max_score = max(max_score, part1(parsed_input, 2, r, 0))
	
	# Right axis
	for r in range(nrows):
		max_score = max(max_score, part1(parsed_input, 0, r, ncols-1))

	# Top axis
	for c in range(ncols):
		max_score = max(max_score, part1(parsed_input, 3, 0, c))

	# Bottom axis
	for c in range(ncols):
		max_score = max(max_score, part1(parsed_input, 1, nrows-1, c))

	return max_score

if __name__ == "__main__":
	for filename in sys.argv[1:]:
		print(f'Filename: {filename}')
		parsed_input = parse(filename)

		# Solving today's puzzles
		print(f'Part one: {part1(parsed_input, 2, 0, 0)}')
		print(f'Part two: {part2(parsed_input)}')
