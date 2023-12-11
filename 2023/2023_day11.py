# Python file for solving the puzzles of day 11 of Advent of Code 2023
import itertools as it
import numpy as np
import sys
import re

def compute_distance(g1, g2, empty_columns, empty_rows, part_one):
	miny, maxy, minx, maxx = min(g1[0], g2[0]), max(g1[0], g2[0]), min(g1[1], g2[1]), max(g1[1], g2[1])
	if part_one:
		return abs(maxy - miny) + abs(maxx - minx) + sum(i in empty_rows for i in range(miny+1,maxy)) + sum(j in empty_columns for j in range(minx+1,maxx))
	else:
		return abs(maxy - miny) + abs(maxx - minx) + 999_999 * (sum(i in empty_rows for i in range(miny+1,maxy)) + sum(j in empty_columns for j in range(minx+1,maxx)))

def parse(puzzle_input):
	'''Method for parsing the puzzle input into a more suitable format for computations'''
	mapping = {'.': 0, '#': 1}
	with open(puzzle_input, 'r+') as f:
		parsed_input = np.array([[mapping[x] for x in line.strip()] for line in f.readlines()])
	return parsed_input

def part1(arr):
	empty_columns = set(np.where(~arr.any(axis=0))[0])
	empty_rows = set(np.where(~arr.any(axis=1))[0])
	x_galaxies, y_galaxies = np.where(arr==1)
	galaxies = zip(x_galaxies, y_galaxies)

	return sum(compute_distance(g1, g2, empty_columns, empty_rows, True) for (g1, g2) in it.combinations(galaxies, r=2))

def part2(arr):
	empty_columns = set(np.where(~arr.any(axis=0))[0])
	empty_rows = set(np.where(~arr.any(axis=1))[0])
	x_galaxies, y_galaxies = np.where(arr==1)
	galaxies = list(zip(x_galaxies, y_galaxies))

	return sum(compute_distance(g1, g2, empty_columns, empty_rows, False) for (g1, g2) in it.combinations(galaxies, r=2))

if __name__ == "__main__":
	for filename in sys.argv[1:]:
		print(f'Filename: {filename}')
		parsed_input = parse(filename)

		# Solving today's puzzles
		print(f'Part one: {part1(parsed_input)}')
		print(f'Part two: {part2(parsed_input)}')
