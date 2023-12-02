# Python file for solving the puzzles of day 1 of Advent of Code 2023
from functools import reduce
import itertools as it
import numpy as np
import sys
import re

def parse(filename):
	'''Method for parsing the puzzle input into a more suitable format for computations'''
	with open(filename, 'r+') as f:
		parsed_input = list(map(str.strip, f.readlines()))
	return parsed_input

def part1(parsed_input):
	result = 0
	for line in parsed_input:
		digits = re.findall('\d', line)
		if len(digits):
			result += int(digits[0] + digits[-1])
	return result

def part2(parsed_input):
	mapping = {
		'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5', 'six': '6', 'seven': '7', 'eight': '8', 'nine': '9'
	}
	pattern = '|'.join(mapping.keys())
	# print(pattern)
	
	result = 0
	for line in parsed_input:
		# Look for digit word at start
		first_digit_pattern = "\d|" + "|".join(mapping.keys())
		first_digit = re.findall(first_digit_pattern, line)[0]
		if first_digit in mapping:
			first_digit = mapping[first_digit]

		final_digit_pattern = "\d|" + "|".join(s[::-1] for s in mapping.keys())
		reversed_line = line[::-1]
		final_digit = re.findall(final_digit_pattern, reversed_line)[0]
		if final_digit[::-1] in mapping:
			final_digit = mapping[final_digit[::-1]]
		
		result += int(first_digit + final_digit)
	return result
if __name__ == "__main__":
	for filename in sys.argv[1:]:
		print(f'Filename: {filename}')
		parsed_input = parse(filename)

		# Solving today's puzzles
		print(f'Part one: {part1(parsed_input)}')
		print(f'Part two: {part2(parsed_input)}')
