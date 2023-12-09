# Python file for solving the puzzles of day 6 of Advent of Code 2023
import itertools as it
import numpy as np
import sys
import re

def parse(puzzle_input):
	'''Method for parsing the puzzle input into a more suitable format for computations'''
	with open(puzzle_input, 'r+') as f:
		parsed_input = list(map(str.strip, f.readlines()))
		record_times = list(map(int, re.findall('\d+', parsed_input[0])))
		record_distances = list(map(int, re.findall('\d+', parsed_input[1])))
	return record_times, record_distances

def part1(record_times, record_distances):
	num = 1
	for race_idx in range(len(record_times)):
		time, distance = record_times[race_idx], record_distances[race_idx]
		num *= sum(x * (time - x) > distance for x in range(time))
	return num

def part2(record_times, record_distances):
	time = int(''.join(map(str, record_times)))
	distance = int(''.join(map(str, record_distances)))
	
	# BINARY SEARCH FOR SMALLEST ELEMENT
	start_smallest, end_smallest = 0, time
	while start_smallest < end_smallest:
		mid = (start_smallest + end_smallest) // 2
		if mid == start_smallest:
			break
		if mid * (time - mid) > distance:
			end_smallest = mid
		else:
			start_smallest = mid + 1

	start_largest, end_largest = 0, time
	while start_largest < end_largest:
		mid = (start_largest + end_largest) // 2
		if mid == start_largest:
			break
		if mid * (time - mid) > distance:
			start_largest = mid
		else:
			end_largest = mid - 1
	
	return start_largest - start_smallest + 1

if __name__ == "__main__":
	for filename in sys.argv[1:]:
		print(f'Filename: {filename}')
		record_times, record_distances = parse(filename)

		# Solving today's puzzles
		print(f'Part one: {part1(record_times, record_distances)}')
		print(f'Part two: {part2(record_times, record_distances)}')
