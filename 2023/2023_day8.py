# Python file for solving the puzzles of day 8 of Advent of Code 2023
import itertools as it
import numpy as np
import sys
import re
import math
from functools import reduce

def parse(puzzle_input):
	'''Method for parsing the puzzle input into a more suitable format for computations'''
	with open(puzzle_input, 'r+') as f:
		parsed_input = list(map(str.strip, f.readlines()))
		directions = parsed_input[0]
		neighbours = {}
		for line in parsed_input[2:]:
			src, left, right = re.findall('[A-Z0-9]+', line)
			neighbours[src] = (left, right)
	return directions, neighbours

def part1(directions, neighbours):
	current_pos = 'AAA'
	steps = 0
	for d in it.cycle(directions):
		steps += 1
		current_pos = neighbours[current_pos][d == 'R']
		if current_pos == 'ZZZ':
			return steps

def part2(directions, neighbours):
	current_positions = [node for node in neighbours.keys() if node[-1]=='A']
	computed_steps = []

	for pos in current_positions:
		new_pos = pos
		steps = 0
		for d in it.cycle(directions):
			steps += 1
			new_pos = neighbours[new_pos][d == 'R']
			if new_pos[-1] == 'Z':
				computed_steps.append(steps)
				break
	return reduce(lambda x,y: (x*y) // math.gcd(x,y), computed_steps)

if __name__ == "__main__":
	for filename in sys.argv[1:]:
		print(f'Filename: {filename}')
		directions, neighbours = parse(filename)

		# Solving today's puzzles
		# print(f'Part one: {part1(directions, neighbours)}')
		print(f'Part two: {part2(directions, neighbours)}')
