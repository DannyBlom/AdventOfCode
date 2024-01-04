# Python file for solving the puzzles of day 22 of Advent of Code 2023
import itertools as it
import numpy as np
import sys
import re
from copy import deepcopy

def can_be_disintegrated(rest_graph, current):
	resting_bricks = set(rest_graph[current])
	supported_bricks = set()
	for idx in rest_graph:
		if idx == current:
			continue
		for brick in resting_bricks:
			if brick in rest_graph[idx]:
				supported_bricks.add(brick)
	
	return len(resting_bricks) == len(supported_bricks)

def parse(puzzle_input):
	'''Method for parsing the puzzle input into a more suitable format for computations'''
	with open(puzzle_input, 'r+') as f:
		parsed_input = {}
		for idx, line in enumerate(f.readlines()):
			x1, y1, z1, x2, y2, z2 = map(int, re.search('(\d+),(\d+),(\d+)\~(\d+),(\d+),(\d+)', line).groups())
			brick_positions = {(x,y,z) for x in range(x1, x2+1) for y in range(y1, y2+1) for z in range(z1, z2+1)}
			parsed_input[idx] = {'brick_positions': brick_positions, 'min_z': z1}
	return parsed_input

def part1(parsed_input):
	filled_brick_index = {} # key: position of brick piece, value: brick index
	floating_bricks = set(parsed_input.keys())
	rest_graph = {i: set() for i in floating_bricks}

	while floating_bricks:
		current = min(floating_bricks, key=lambda x: parsed_input[x]['min_z'])
		floating_bricks.discard(current)
		while True:
			fall = True
			for (x,y,z) in parsed_input[current]['brick_positions']:
				if z == 1:
					fall = False
					break

				if (x,y,z-1) in filled_brick_index:
					fall = False
					rest_graph[filled_brick_index[x,y,z-1]].add(current)
			
			if fall:
				parsed_input[current]['brick_positions'] = set((x,y,z-1) for (x,y,z) in parsed_input[current]['brick_positions'])
				parsed_input[current]['min_z'] -= 1
			else:
				for (x,y,z) in parsed_input[current]['brick_positions']:
					filled_brick_index[x,y,z] = current
				break
	return rest_graph, sum(can_be_disintegrated(rest_graph, current) for current in parsed_input.keys())

def chain_reaction(reversed_graph, idx):
	num_supporting_bricks = {k: len(reversed_graph[k]) for k in reversed_graph}
	removed_supporting_bricks = {k: 0 for k in reversed_graph}
	score = 0

	fallen_bricks = {k for k in num_supporting_bricks if num_supporting_bricks[k] == 0}
	for k in reversed_graph:
		if idx in reversed_graph[k]:
			removed_supporting_bricks[k] += 1
	
	bricks_to_process = set(k for k in reversed_graph.keys() if num_supporting_bricks[k] == removed_supporting_bricks[k])
	while bricks_to_process:
		current = bricks_to_process.pop()
		if current in fallen_bricks:
			bricks_to_process.discard(current)
			continue

		score += 1
		fallen_bricks.add(current)
		for k in reversed_graph:
			if current in reversed_graph[k]:
				removed_supporting_bricks[k] += 1
				if num_supporting_bricks[k] == removed_supporting_bricks[k]:
					bricks_to_process.add(k)
		
	return score

def part2(parsed_input, rest_graph):
	reversed_graph = {k: set() for k in parsed_input.keys()}
	for k in rest_graph:
		for v in rest_graph[k]:
			reversed_graph[v].add(k)
	
	return sum(chain_reaction(reversed_graph, idx) for idx in rest_graph)


if __name__ == "__main__":
	for filename in sys.argv[1:]:
		print(f'Filename: {filename}')
		parsed_input = parse(filename)

		# Solving today's puzzles
		rest_graph, sol1 = part1(parsed_input)
		print(f'Part one: {sol1}')
		print(f'Part two: {part2(parsed_input, rest_graph)}')
