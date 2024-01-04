# Python file for solving the puzzles of day 14 of Advent of Code 2023
import itertools as it
import numpy as np
import sys
import re

def tilt_north(parsed_input, ncols, nrows):
	for c in range(ncols):
		new_column = []
		for r in range(nrows):
			current_cell = parsed_input[r][c]
			if current_cell == 'O':
				new_column.append('O')
			elif current_cell == '#':
				while len(new_column) < r:
					new_column.append('.')
				new_column.append('#')
		while len(new_column) < nrows:
			new_column.append('.')
		parsed_input[:,c] = new_column
	return parsed_input

def tilt_west(parsed_input, ncols, nrows):
	for r in range(nrows):
		new_row = []
		for c in range(ncols):
			current_cell = parsed_input[r][c]
			if current_cell == 'O':
				new_row.append('O')
			elif current_cell == '#':
				while len(new_row) < c:
					new_row.append('.')
				new_row.append('#')
		while len(new_row) < ncols:
			new_row.append('.')
		parsed_input[r,:] = new_row
	return parsed_input

def tilt_south(parsed_input, ncols, nrows):
	for c in range(ncols):
		new_column = []
		for r in range(nrows):
			current_cell = parsed_input[nrows-r-1][c]
			if current_cell == 'O':
				new_column.append('O')
			elif current_cell == '#':
				while len(new_column) < r:
					new_column.append('.')
				new_column.append('#')
		while len(new_column) < nrows:
			new_column.append('.')
		parsed_input[:,c] = new_column[::-1]
	return parsed_input

def tilt_east(parsed_input, ncols, nrows):
	for r in range(nrows):
		new_row = []
		for c in range(ncols):
			current_cell = parsed_input[r][ncols-1-c]
			if current_cell == 'O':
				new_row.append('O')
			elif current_cell == '#':
				while len(new_row) < c:
					new_row.append('.')
				new_row.append('#')
		while len(new_row) < ncols:
			new_row.append('.')
		parsed_input[r,:] = new_row[::-1]
	return parsed_input
			
def parse(puzzle_input):
	'''Method for parsing the puzzle input into a more suitable format for computations'''
	with open(puzzle_input, 'r+') as f:
		parsed_input = np.array([[x for x in line.strip()] for line in f.readlines()])
	return parsed_input

def perform_iteration(parsed_input):
	nrows, ncols = parsed_input.shape
	for fnc in (tilt_north, tilt_west, tilt_south, tilt_east):
		parsed_input = fnc(parsed_input, ncols, nrows)
	return parsed_input

def part1(parsed_input):
	nrows, ncols = parsed_input.shape 
	parsed_input = tilt_north(parsed_input, ncols, nrows)
	score = 0
	for c in range(ncols):
		for r in range(nrows):
			if parsed_input[r][c] == 'O':
				score += (nrows - r)
	return score

def part2(parsed_input):
	nrows, ncols = parsed_input.shape
	iter = 0
	state_observation_iter = {''.join(parsed_input[r][c] for (r,c) in it.product(range(nrows), range(ncols))) : iter} # key: state, value: iteration_nr
	iter_states = {iter: ''.join(parsed_input[r][c] for (r,c) in it.product(range(nrows), range(ncols)))}
	while iter < 1_000_000_000:
		iter += 1
		parsed_input = perform_iteration(parsed_input)
		state = ''.join(parsed_input[r][c] for (r,c) in it.product(range(nrows), range(ncols)))
		if state in state_observation_iter:
			last_iter = state_observation_iter[state]
			break
		state_observation_iter[state] = iter
		iter_states[iter] = state

	cycle_length = iter - last_iter
	print(f'Last iter {last_iter} and current iter {iter}')
	print(f'Cycle length: {cycle_length}')
	
	equivalence_class = (1_000_000_000 - last_iter) % cycle_length
	final_state = iter_states[last_iter + equivalence_class]

	# Find corresponding array
	arr = []
	for r in range(nrows):
		row = []
		for c in range(ncols):
			row.append(final_state[ncols * r + c])
		arr.append(row)
	parsed_input = np.array(arr)
			

	score = 0
	for c in range(ncols):
		for r in range(nrows):
			if parsed_input[r][c] == 'O':
				score += (nrows - r)
	return score

if __name__ == "__main__":
	for filename in sys.argv[1:]:
		print(f'Filename: {filename}')
		parsed_input = parse(filename)

		# Solving today's puzzles
		print(f'Part one: {part1(parsed_input)}')
		print(f'Part two: {part2(parsed_input)}')
