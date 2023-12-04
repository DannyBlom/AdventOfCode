# Python file for solving the puzzles of day 3 of Advent of Code 2023
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
	global symbol_positions
	global start_ints
	global end_ints

	digits = '1234567890'
	digits_or_empty = '.' + digits

	symbol_positions = set()
	start_ints = []
	end_ints = []
	
	for row in range(len(parsed_input)):
		for col in range(len(parsed_input[row])):
			if parsed_input[row][col] not in digits_or_empty:
				symbol_positions.add((row, col))
				continue
			if parsed_input[row][col] in digits:
				if col == 0 or (col >= 1 and parsed_input[row][col-1] not in digits):
					start_ints.append((row,col))
				if col == len(parsed_input[row]) - 1 or (col < len(parsed_input[row]) - 1 and parsed_input[row][col+1] not in digits):
					end_ints.append((row,col)) 
	score = 0
	for ((rs,cs), (re,ce)) in zip(start_ints, end_ints):
		assert rs == re
		row_range = range(max(rs-1,0), min(rs+2, len(parsed_input)))
		col_range = range(max(cs-1,0), min(ce+2, len(parsed_input[0])))

		if sum(parsed_input[a][b] not in digits_or_empty for a in row_range for b in col_range) >= 1:
			score += int(parsed_input[rs][cs:(ce+1)])
	return score

def part2(parsed_input):
	possible_gears = set(filter(lambda x: parsed_input[x[0]][x[1]] == '*', symbol_positions))
	score = 0
	for (rg, cg) in possible_gears:
		adjacent_numbers = set()
		for ((rs,cs), (re,ce)) in zip(start_ints, end_ints):
			columns = list(range(cs, ce+1))
			if rs in range(rg-1, rg+2) and (cg-1 in columns or cg in columns or cg+1 in columns):
				adjacent_numbers.add(((rs,cs),(re,ce)))
		
		gear_ratio = 1
		if len(adjacent_numbers) == 2:
			for ((rs,cs),(re,ce)) in adjacent_numbers:
				gear_ratio *= int(parsed_input[rs][cs:(ce+1)])
			score += gear_ratio
	return score

if __name__ == "__main__":
	for filename in sys.argv[1:]:
		print(f'Filename: {filename}')
		parsed_input = parse(filename)
		print(parsed_input, len(parsed_input))

		# Solving today's puzzles
		print(f'Part one: {part1(parsed_input)}')
		print(f'Part two: {part2(parsed_input)}')
