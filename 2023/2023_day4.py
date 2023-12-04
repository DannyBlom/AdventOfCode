# Python file for solving the puzzles of day 4 of Advent of Code 2023
import itertools as it
import numpy as np
import sys
import re

def parse(puzzle_input):
	'''Method for parsing the puzzle input into a more suitable format for computations'''
	with open(puzzle_input, 'r+') as f:
		parsed_input = []
		for line in f.readlines():
			line = line.split(': ')[1]
			line = line.split('|')
			parsed_input.append(line)
	return parsed_input

def part1(parsed_input):
	score = 0
	for line in parsed_input:
		winning_numbers = set(map(int, re.findall('\d+', line[0])))
		own_numbers = set(map(int, re.findall('\d+', line[1])))
		num_own_winning_numbers = sum(num in winning_numbers for num in own_numbers)
		if not num_own_winning_numbers == 0:
			score += 2 ** (num_own_winning_numbers - 1)
	return score

def part2(parsed_input):
	num_cards = {i: 1 for i in range(len(parsed_input))}
	maxkey = max(num_cards.keys())
	score = 0
	for idx, line in enumerate(parsed_input):
		winning_numbers = set(map(int, re.findall('\d+', line[0])))
		own_numbers = set(map(int, re.findall('\d+', line[1])))
		num_own_winning_numbers = sum(num in winning_numbers for num in own_numbers)

		num_current_card = num_cards[idx]
		score += num_current_card
		for l in range(num_own_winning_numbers):
			if l < maxkey:
				num_cards[idx + 1 + l] += num_current_card
	return score		
			
if __name__ == "__main__":
	for filename in sys.argv[1:]:
		print(f'Filename: {filename}')
		parsed_input = parse(filename)

		# Solving today's puzzles
		print(f'Part one: {part1(parsed_input)}')
		print(f'Part two: {part2(parsed_input)}')
