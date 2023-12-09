# Python file for solving the puzzles of day 9 of Advent of Code 2023
import itertools as it
import numpy as np
import sys
import re

def parse(puzzle_input):
	'''Method for parsing the puzzle input into a more suitable format for computations'''
	with open(puzzle_input, 'r+') as f:
		parsed_input = [ list(map(int, re.findall('-?\d+', line))) for line in f.readlines() ]
	return parsed_input

def part1(parsed_input):
	result = 0
	for line in parsed_input:
		idx = 0
		difference_lst = [line]
		current_seq = line
		while len(current_seq):
			differences = [current_seq[i+1] - current_seq[i] for i in range(len(current_seq) - 1)]
			difference_lst.append(differences)
			idx += 1
			current_seq = differences
			if sum(d == 0 for d in current_seq) == len(current_seq):
				break
		
		value = 0
		for k in range(idx-1, -1, -1):
			value += difference_lst[k][-1]
		result += value
	return result

def part2(parsed_input):
	result = 0
	for line in parsed_input:
		idx = 0
		difference_lst = [line]
		current_seq = line
		while len(current_seq):
			differences = [current_seq[i+1] - current_seq[i] for i in range(len(current_seq) - 1)]
			difference_lst.append(differences)
			idx += 1
			current_seq = differences
			if sum(d == 0 for d in current_seq) == len(current_seq):
				break
		
		value = 0
		for k in range(idx-1, -1, -1):
			value = difference_lst[k][0] - value
		result += value
	return result

if __name__ == "__main__":
	for filename in sys.argv[1:]:
		print(f'Filename: {filename}')
		parsed_input = parse(filename)

		# Solving today's puzzles
		print(f'Part one: {part1(parsed_input)}')
		print(f'Part two: {part2(parsed_input)}')
