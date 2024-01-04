# Python file for solving the puzzles of day 17 of Advent of Code 2023
import itertools as it
import numpy as np
import sys
import re
import math 
import heapq

def parse(puzzle_input):
	'''Method for parsing the puzzle input into a more suitable format for computations'''
	with open(puzzle_input, 'r+') as f:
		parsed_input = np.array([[int(x) for x in line.strip()] for line in f.readlines()])
	return parsed_input

def new_positions(parsed_input, item, directions, part_one):
	nrows, ncols = parsed_input.shape
	val, y, x, last_dir = item
	if last_dir == -1:
		# First step, so we are in left upper corner
		arr = [2,3]
	else:
		arr = [(last_dir + 1) % 4, (last_dir + 3) % 4]
	
	for d in arr:
		score = 0
		inc_y, inc_x = directions[d]

		if part_one:
			for i in range(1, 4):
				new_y = y + i*inc_y
				new_x = x + i*inc_x

				if 0 <= new_y < nrows and 0 <= new_x < ncols:
					score += parsed_input[new_y, new_x]
					yield (val+score, new_y, new_x, d)
		else:
			for i in range(1, 11):
				new_y = y + i*inc_y
				new_x = x + i*inc_x
				if 0 <= new_y < nrows and 0 <= new_x < ncols:
					score += parsed_input[new_y, new_x]
					if i >= 4:
						yield (val+score, new_y, new_x, d)
				else:
					break
				

def part1(parsed_input):
	nrows, ncols = parsed_input.shape
	directions = {0: (0, -1), 1: (-1, 0), 2: (0, 1), 3: (1, 0)}
	queue = []
	heapq.heappush(queue, (0,0,0,-1))
	min_val = math.inf

	shortest_distances = {(y,x,t): math.inf for y in range(nrows) for x in range(ncols) for t in range(2)}
	iter = 0
	while queue:
		iter += 1
		val, y, x, last_dir = heapq.heappop(queue)

		if last_dir >= 0:
			if y == nrows - 1 and x == ncols - 1:
				print(val, y, x, last_dir)
				if val < min_val:
					min_val = val
					shortest_distances[y,x,last_dir % 2] = val
					continue

			if val >= min_val:
				continue
			
			if val >= shortest_distances[y, x, last_dir % 2]:
				continue

			shortest_distances[y, x, last_dir % 2] = val

		item = (val, y, x, last_dir)
		for new_item in new_positions(parsed_input, item, directions, True):
			heapq.heappush(queue, new_item)
			
	return min_val
		

def part2(parsed_input):
	nrows, ncols = parsed_input.shape
	directions = {0: (0, -1), 1: (-1, 0), 2: (0, 1), 3: (1, 0)}
	queue = []
	heapq.heappush(queue, (0,0,0,-1))
	min_val = math.inf

	shortest_distances = {(y,x,t): math.inf for y in range(nrows) for x in range(ncols) for t in range(2)}
	iter = 0
	while queue:
		iter += 1
		val, y, x, last_dir = heapq.heappop(queue)

		if last_dir >= 0:
			if y == nrows - 1 and x == ncols - 1:
				print(val, y, x, last_dir)
				if val < min_val:
					min_val = val
					shortest_distances[y,x,last_dir % 2] = val
					continue

			if val >= min_val:
				continue
			
			if val >= shortest_distances[y, x, last_dir % 2]:
				continue

			shortest_distances[y, x, last_dir % 2] = val

		item = (val, y, x, last_dir)
		for new_item in new_positions(parsed_input, item, directions, False):
			heapq.heappush(queue, new_item)
			
	return min_val

if __name__ == "__main__":
	for filename in sys.argv[1:]:
		print(f'Filename: {filename}')
		parsed_input = parse(filename)

		# Solving today's puzzles
		print(f'Part one: {part1(parsed_input)}')
		print(f'Part two: {part2(parsed_input)}')
