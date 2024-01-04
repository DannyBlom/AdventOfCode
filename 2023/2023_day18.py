# Python file for solving the puzzles of day 18 of Advent of Code 2023
import itertools as it
import numpy as np
import networkx as nx
import sys
import re
from shapely.geometry import Polygon

def neighbours(current_cell, min_y, max_y, min_x, max_x):
	y, x = current_cell
	if y - 1 >= min_y:
		yield (y-1,x)
	if y + 1 <= max_y:
		yield (y+1,x)
	if x-1 >= min_x:
		yield (y,x-1)
	if x+1 <= max_x:
		yield (y,x+1)

def parse(puzzle_input):
	'''Method for parsing the puzzle input into a more suitable format for computations'''
	with open(puzzle_input, 'r+') as f:
		parsed_input = f.readlines()
	return parsed_input

def part1(parsed_input):
	directions = {'D': (1, 0), 'U': (-1, 0), 'L': (0, -1), 'R': (0, 1) }
	dug_trenches = set()
	current_y, current_x = 0, 0

	for line in parsed_input:
		d, num, hexcode = line.split()
		for _ in range(int(num)):
			dug_trenches.add( (current_y, current_x) )
			dir_incs = directions[d]
			current_y += dir_incs[0]
			current_x += dir_incs[1]
	
	min_y = min(x[0] for x in dug_trenches)
	max_y = max(x[0] for x in dug_trenches)
	min_x = min(x[1] for x in dug_trenches)
	max_x = max(x[1] for x in dug_trenches)
	
	boundary_box_surface = (max_y - min_y + 1) * (max_x - min_x + 1)
	boundary_hor = set((min_y,j) for j in range(min_x, max_x+1)).union(set((max_y,j) for j in range(min_x, max_x+1)))
	boundary_ver = set((i,min_x) for i in range(min_y, max_y+1)).union(set((i,max_x) for i in range(min_y, max_y+1)))
	boundary = boundary_hor.union(boundary_ver)

	num_filled_cells = boundary_box_surface
	visited = set()
	for cell in boundary:
		if cell not in dug_trenches and cell not in visited:
			queue = [cell]
			visited.add(cell)
			while queue:
				current_cell = queue.pop(0)
				for nb in neighbours(current_cell, min_y, max_y, min_x, max_x):
					if nb not in dug_trenches and nb not in visited:
						visited.add(nb)
						queue.append(nb)
	
	return num_filled_cells - len(visited)
		
def part2(parsed_input):
	directions = {0: (0, 1), 1: (1, 0),  2: (0, -1), 3: (-1, 0) } 
	num_dug_trenches = 0
	current_y, current_x = 0, 0

	ys = [current_y]
	xs = [current_x]

	for line in parsed_input:
		d, num, hexcode = line.split()
		hexcode = hexcode.strip('()#')
		dist = int(hexcode[:5], 16)
		num_dug_trenches += dist
		d = int(hexcode[-1])

		current_y += dist*directions[d][0]
		current_x += dist*directions[d][1]
		ys.append(current_y)
		xs.append(current_x)
	
	pgon = Polygon(zip(ys, xs))	

	# Use Pick's theorem to find number of interior points
	num_interior_points = int(pgon.area + 1 - (num_dug_trenches // 2))
	return num_dug_trenches + num_interior_points

if __name__ == "__main__":
	for filename in sys.argv[1:]:
		print(f'Filename: {filename}')
		parsed_input = parse(filename)

		# Solving today's puzzles
		print(f'Part one: {part1(parsed_input)}')
		print(f'Part two: {part2(parsed_input)}')
