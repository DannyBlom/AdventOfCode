# Python file for solving the puzzles of day 21 of Advent of Code 2023
import itertools as it
import numpy as np
import sys
import re
from collections import deque

def neighbours(nrows, ncols, row, col, part_one):
	if part_one:
		if row - 1 in range(nrows):
			yield (row-1,col)
		if row + 1 in range(nrows):
			yield (row+1,col)
		if col - 1 in range(ncols):
			yield (row,col-1)
		if col + 1 in range(ncols):
			yield (row,col+1)
	else:
		yield (row - 1, col)
		yield (row + 1, col)
		yield (row, col - 1)
		yield (row, col + 1)

def parse(puzzle_input):
	'''Method for parsing the puzzle input into a more suitable format for computations'''
	with open(puzzle_input, 'r+') as f:
		parsed_input = np.array([[x for x in line.strip()] for line in f.readlines()])
	return parsed_input

def part1(parsed_input, remaining_steps):
	nrows, ncols = parsed_input.shape
	position_S = np.where(parsed_input == 'S')
	start_position = position_S[0][0], position_S[1][0]
	shortest_distances = {start_position: 0}
	num_destinations = (remaining_steps % 2 == 0)
	
	queue = deque()
	queue.append((start_position, 0))
	max_num_steps = -1 
	while len(queue) and max_num_steps <= remaining_steps:
		current_pos, num_steps = queue.popleft()
		
		if num_steps > max_num_steps:
			max_num_steps = num_steps

		if num_steps < remaining_steps:
			for nb in neighbours(nrows, ncols, *current_pos, True):
				if nb in shortest_distances:
					continue
				elif parsed_input[nb] == '.':
					shortest_distances[nb] = num_steps + 1
					queue.append((nb, num_steps+1))
					if (num_steps + 1) % 2 == remaining_steps % 2:
						num_destinations += 1
	
	return num_destinations

def explore_unbounded(parsed_input, remaining_steps):
	nrows, ncols = parsed_input.shape
	position_S = np.where(parsed_input == 'S')
	start_position = position_S[0][0], position_S[1][0]
	shortest_distances = {start_position: 0}
	num_destinations = (remaining_steps % 2 == 0)
	
	queue = deque()
	queue.append((start_position, 0))
	max_num_steps = -1
	while len(queue) and max_num_steps <= remaining_steps:
		current_pos, num_steps = queue.popleft()
		
		if num_steps > max_num_steps:
			max_num_steps = num_steps

		if num_steps < remaining_steps:
			for nb in neighbours(nrows, ncols, *current_pos, False):
				if nb in shortest_distances:
					continue
				
				orow, ocol = nb[0] % nrows, nb[1] % ncols
				if parsed_input[orow, ocol] == '#':
					continue
				else:
					shortest_distances[nb] = num_steps + 1
					queue.append((nb, num_steps+1))
					if (num_steps + 1) % 2 == remaining_steps % 2:
						num_destinations += 1
	
	return num_destinations

def part2(parsed_input, remaining_steps):
	points = [(i, explore_unbounded(parsed_input, 65 + 131*i)) for i in range(3)]

	def evaluate_quadratic_equation(points, x):
		# Fit a quadratic polynomial (degree=2) through the points
		coefficients = np.polyfit(*zip(*points), 2)

		# Evaluate the quadratic equation at the given x value
		result = np.polyval(coefficients, x)
		return round(result)

	return evaluate_quadratic_equation(points, 202300) 

if __name__ == "__main__":
	for filename in sys.argv[1:]:
		print(f'Filename: {filename}')
		parsed_input = parse(filename)

		# Solving today's puzzles
		print(f'Part one: {part1(parsed_input, 64)}')
		print(f'Part two: {part2(parsed_input, 26501365)}')
