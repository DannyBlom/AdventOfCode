# Python file for solving the puzzles of day 23 of Advent of Code 2023
import itertools as it
import networkx as nx
import numpy as np
import sys
import re

def neighbours(parsed_input, nrows, ncols, i, j):
	nbs, directions = [], []
	if i - 1 in range(nrows) and parsed_input[i-1,j] != '#':
		nbs.append((i-1,j))
		directions.append(1)
	if i + 1 in range(nrows) and parsed_input[i+1,j] != '#':
		nbs.append((i+1,j))
		directions.append(3)
	if j - 1 in range(ncols) and parsed_input[i,j-1] != '#':
		nbs.append((i,j-1))
		directions.append(0)
	if j + 1 in range(ncols) and parsed_input[i,j+1] != '#':
		nbs.append((i,j+1))
		directions.append(2)
	return nbs, directions

def greatest_simple_pathlength(graph, source, target):
    longest_path_length = 0
    for path in nx.all_simple_paths(graph, source=source, target=target):
        path_length = sum(graph[path[i]][path[i+1]]['weight'] for i in range(len(path)-1))
        if path_length > longest_path_length:
            longest_path_length = path_length
    return longest_path_length

def parse(puzzle_input):
	'''Method for parsing the puzzle input into a more suitable format for computations'''
	with open(puzzle_input, 'r+') as f:
		parsed_input = np.array([[x for x in line.strip()] for line in f.readlines()])
	return parsed_input

def part1(parsed_input):
	nrows, ncols = parsed_input.shape
	forbidden_slopes = {0: '>', 1: 'v', 2: '<', 3: '^'}
	tiles = set((i,j) for i in range(nrows) for j in range(ncols) if parsed_input[i,j] != '#')
	crossings = set(filter(lambda x: len(neighbours(parsed_input, nrows, ncols, *x)[0]) > 2, tiles))
	crossings.add((0,1)) # add starting point
	crossings.add((nrows-1, ncols-2)) # add end point
	graph = nx.DiGraph()
	for (i, j) in crossings:
		# Investigate segments
		nbs, directions = neighbours(parsed_input, nrows, ncols, i, j)
		for idx, (u, v) in enumerate(nbs):
			visited = set()
			visited.add((i,j))
			visited.add((u,v))
			current = (u,v)
			length = 1

			valid_segment = True
			while current not in crossings:
				current_nbs, current_directions = neighbours(parsed_input, nrows, ncols, *current)
				for curidx, nb in enumerate(current_nbs):
					d = current_directions[curidx]
					if nb not in visited:
						if parsed_input[nb] == forbidden_slopes[d]:
							valid_segment = False
							break
						else:
							visited.add(nb)
							current = nb
							length += 1
							break
				if not valid_segment:
					break
			
			if valid_segment:
				graph.add_edge((i,j), current, weight=length)


	return greatest_simple_pathlength(graph, (0,1), (nrows-1, ncols-2))

def part2(parsed_input):
	nrows, ncols = parsed_input.shape
	tiles = set((i,j) for i in range(nrows) for j in range(ncols) if parsed_input[i,j] != '#')
	crossings = set(filter(lambda x: len(neighbours(parsed_input, nrows, ncols, *x)[0]) > 2, tiles))
	crossings.add((0,1)) # add starting point
	crossings.add((nrows-1, ncols-2)) # add end point
	graph = nx.Graph()
	for (i, j) in crossings:
		# Investigate segments
		nbs, directions = neighbours(parsed_input, nrows, ncols, i, j)
		for (u, v) in nbs:
			visited = set()
			visited.add((i,j))
			visited.add((u,v))
			current = (u,v)
			length = 1

			while current not in crossings:
				current_nbs, current_directions = neighbours(parsed_input, nrows, ncols, *current)
				for nb in current_nbs:
					if nb not in visited:
						visited.add(nb)
						current = nb
						length += 1
						break
			
			graph.add_edge((i,j), current, weight=length)

	return greatest_simple_pathlength(graph, (0,1), (nrows-1, ncols-2))

if __name__ == "__main__":
	for filename in sys.argv[1:]:
		print(f'Filename: {filename}')
		parsed_input = parse(filename)
	
		# Solving today's puzzles
		print(f'Part one: {part1(parsed_input)}')
		print(f'Part two: {part2(parsed_input)}')
