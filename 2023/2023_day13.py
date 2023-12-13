# Python file for solving the puzzles of day 13 of Advent of Code 2023
import itertools as it
import numpy as np
import sys
import re

def find_reflection_score(instance):
	nrows = len(instance)
	ncols = len(instance[0])

	vertical = True
	# First look at vertical reflections
	for i in range(1, ncols):
		# Vertical line left from i
		valid = True
		j = 0
		while i - 1 - j >= 0 and i + j < ncols:
			for k in range(nrows):
				if instance[k][i-1-j] != instance[k][i+j]:
					valid = False
					break
			if not valid:
				break
			j += 1

		if valid:
			return i
	
	# Now look at horizontal reflections
	for i in range(1, nrows):
		# Horitzontal line above row i
		valid = True
		j = 0
		while i - 1 - j >= 0 and i + j < nrows:
			for k in range(ncols):
				if instance[i-1-j][k] != instance[i+j][k]:
					valid = False
					break
			if not valid:
				break
			j += 1

		if valid:
			return 100*i

def find_smudged_reflection_score(instance):
	nrows = len(instance)
	ncols = len(instance[0])

	vertical = True
	# First look at vertical reflections
	for i in range(1, ncols):
		# Vertical line left from i
		nsmudges = 0
		j = 0
		while i - 1 - j >= 0 and i + j < ncols:
			for k in range(nrows):
				if instance[k][i-1-j] != instance[k][i+j]:
					nsmudges += 1
			j += 1

		if nsmudges == 1:
			return i
	
	# Now look at horizontal reflections
	for i in range(1, nrows):
		# Horitzontal line above row i
		nsmudges = 0
		j = 0
		while i - 1 - j >= 0 and i + j < nrows:
			for k in range(ncols):
				if instance[i-1-j][k] != instance[i+j][k]:
					nsmudges += 1
			j += 1

		if nsmudges == 1:
			return 100*i

def parse(puzzle_input):
	'''Method for parsing the puzzle input into a more suitable format for computations'''
	with open(puzzle_input, 'r+') as f:
		instances = []
		instance = []
		for line in f.readlines():
			if line.strip() != '':
				instance.append(list(line.strip()))
			else:
				instances.append(instance)
				instance = []
		instances.append(instance)
	return instances

def part1(instances):
	return sum(find_reflection_score(instance) for instance in instances)

def part2(instances):
	return sum(find_smudged_reflection_score(instance) for instance in instances)

if __name__ == "__main__":
	for filename in sys.argv[1:]:
		print(f'Filename: {filename}')
		parsed_input = parse(filename)

		# Solving today's puzzles
		print(f'Part one: {part1(parsed_input)}')
		print(f'Part two: {part2(parsed_input)}')
