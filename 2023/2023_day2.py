# Python file for solving the puzzles of day 2 of Advent of Code 2023
import itertools as it
import numpy as np
import sys
import re

def parse(puzzle_input):
	'''Method for parsing the puzzle input into a more suitable format for computations'''
	with open(puzzle_input, 'r+') as f:
		parsed_input = list(map(str.strip, f.readlines()))
	return parsed_input

def part1(parsed_input):
	score = 0
	for idx, line in enumerate(parsed_input):
		valid = True
		# Check red
		max_red = max(int(num) for num in re.findall('(\d+) red', line))
		if max_red > UB_RED:
			continue
		max_green = max(int(num) for num in re.findall('(\d+) green', line))
		if max_green > UB_GREEN:
			continue
		max_blue = max(int(num) for num in re.findall('(\d+) blue', line))
		if max_blue > UB_BLUE:
			continue
		score += idx + 1
	return score

def part2(parsed_input):
	score = 0
	for idx, line in enumerate(parsed_input):
		max_red = max(int(num) for num in re.findall('(\d+) red', line))
		max_green = max(int(num) for num in re.findall('(\d+) green', line))
		max_blue = max(int(num) for num in re.findall('(\d+) blue', line))
		score += max_red * max_green * max_blue
	return score

if __name__ == "__main__":
	global UB_RED
	global UB_BLUE
	global UB_GREEN

	UB_RED, UB_GREEN, UB_BLUE = 12, 13, 14
	for filename in sys.argv[1:]:
		print(f'Filename: {filename}')
		parsed_input = parse(filename)

		# Solving today's puzzles
		print(f'Part one: {part1(parsed_input)}')
		print(f'Part two: {part2(parsed_input)}')
