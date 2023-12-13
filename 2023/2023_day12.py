# Python file for solving the puzzles of day 12 of Advent of Code 2023
import itertools as it
import numpy as np
import sys
import re

def number_of_arrangements(row, seqlens):
	str_seqlens = ','.join(str(i) for i in seqlens)
	if (row, str_seqlens) in dp:
		return dp[row, str_seqlens]

	if not len(row):
		dp[row, str_seqlens] = len(seqlens) == 0
		return len(seqlens) == 0
	
	if len(seqlens) == 0:
		dp[row, str_seqlens] = 1 - ('#' in row)
		return 1 - ('#' in row)
	
	if len(row) < seqlens[0]:
		dp[row, str_seqlens] = 0
		return 0
	
	# If the first character is a dot, we can ignore it
	first_char = row[0]
	if first_char == '.':
		dp[row, str_seqlens] = number_of_arrangements(row[1:], seqlens)
		return number_of_arrangements(row[1:], seqlens)
	
	else:
		valid_start = True
		seqlen = seqlens[0]
		for i in range(seqlen):
			if row[i] == '.':
				valid_start = False
				break
		if valid_start and len(row) > seqlen and row[seqlen] == '#':
			valid_start = False
		
		if first_char == '#':
			if valid_start:
				dp[row, str_seqlens] = number_of_arrangements(row[(seqlen+1):], seqlens[1:])
				return number_of_arrangements(row[(seqlen+1):], seqlens[1:])
			else:
				dp[row, str_seqlens] = 0 
				return 0
			
		else:
			if valid_start:
				dp[row, str_seqlens] = number_of_arrangements(row[1:], seqlens) + number_of_arrangements(row[(seqlen+1):], seqlens[1:])	
				return number_of_arrangements(row[1:], seqlens) + number_of_arrangements(row[(seqlen+1):], seqlens[1:])	
			else:
				dp[row, str_seqlens] = number_of_arrangements(row[1:], seqlens)
				return number_of_arrangements(row[1:], seqlens)
		
def parse(puzzle_input):
	'''Method for parsing the puzzle input into a more suitable format for computations'''
	with open(puzzle_input, 'r+') as f:
		parsed_input = []
		for line in f.readlines():
			row, sequence_lengths = line.split()
			sequence_lengths = list(int(i) for i in sequence_lengths.split(','))
			parsed_input.append((row, sequence_lengths))
	return parsed_input

def part1(parsed_input):
	score = 0
	for line in parsed_input:
		value = number_of_arrangements(*line)
		score += value
	return score

def part2(parsed_input):
	score = 0
	for (row, seqlens) in parsed_input:
		row = '?'.join(row for _ in range(5))
		row = re.sub('\.+', '.', row)
		seqlens = [i for _ in range(5) for i in seqlens]
		print(row, seqlens)
		score += number_of_arrangements(row, seqlens)
	return score

if __name__ == "__main__":
	global dp
	dp = {}

	for filename in sys.argv[1:]:
		print(f'Filename: {filename}')
		parsed_input = parse(filename)

		
		# Solving today's puzzles
		print(f'Part one: {part1(parsed_input)}')
		print(f'Part two: {part2(parsed_input)}')
