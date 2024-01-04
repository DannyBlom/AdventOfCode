# Python file for solving the puzzles of day 15 of Advent of Code 2023
import itertools as it
import numpy as np
import sys
import re

def hash_algorithm(input_string):
	value = 0
	for c in input_string:
		value += ord(c)
		value *= 17
		value %= 256
	return value

def parse(puzzle_input):
	'''Method for parsing the puzzle input into a more suitable format for computations'''
	with open(puzzle_input, 'r+') as f:
		parsed_input = f.readlines()[0].split(',')
	return parsed_input

def part1(parsed_input):
	return sum(hash_algorithm(input_string) for input_string in parsed_input)

def part2(parsed_input):
	boxes = {i : {} for i in range(256)}
	for input_string in parsed_input:
		if '-' in input_string:
			label, focal_length = input_string.split('-')
			operation = '-'
		else:
			label, focal_length = input_string.split('=')
			operation = '='
		
		value = hash_algorithm(label)
		# print(f'Current box {value}')
		if operation == '-':
			if label in boxes[value]:
				del boxes[value][label]
		else:
			if label in boxes[value]:
				boxes[value][label] = focal_length
			else:
				boxes[value][label] = focal_length
		
		# print(f'Boxes: {boxes}')
	
	score = 0
	for i in boxes:
		box_factor = i + 1
		for idx, v in enumerate(boxes[i].values()):
			slot_factor = idx + 1
			focal_length = v
			score += box_factor * slot_factor * int(focal_length)
	return score


		


if __name__ == "__main__":
	for filename in sys.argv[1:]:
		print(f'Filename: {filename}')
		parsed_input = parse(filename)

		# Solving today's puzzles
		print(f'Part one: {part1(parsed_input)}')
		print(f'Part two: {part2(parsed_input)}')
