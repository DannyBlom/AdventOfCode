# Python file for solving the puzzles of day 10 of Advent of Code 2023
import itertools as it
import numpy as np
import networkx as nx
import sys
import re

def determine_initial_direction(parsed_input, ystart, xstart):
	if parsed_input[ystart,xstart-1] in '-LF':
		# Go left
		return 0
	elif parsed_input[ystart-1,xstart] in '|7F':
		# Go up
		return 1
	elif parsed_input[ystart, xstart+1] in '-J7':
		# Go right
		return 2
	else:
		return 3	

def parse(puzzle_input):
	'''Method for parsing the puzzle input into a more suitable format for computations'''
	with open(puzzle_input, 'r+') as f:
		parsed_input = np.array([[x for x in line.strip()] for line in f.readlines()])
	return parsed_input

def part1(parsed_input):
	ystart, xstart = np.where(parsed_input=='S')
	ystart, xstart = ystart[0], xstart[0]
	loop_locations.add( (2*ystart, 2*xstart) ) # We double the coordinates, used for counting inside cells for part 2!
	direction = determine_initial_direction(parsed_input, ystart, xstart)
	change = increments[direction]
	loop_locations.add( (2*ystart + change[0], 2*xstart + change[1]) )
	loop_locations.add( (2*ystart + 2*change[0], 2*xstart + 2*change[1]) )
	current_y = ystart + change[0]
	current_x = xstart + change[1]
	num_steps = 1

	while current_y != ystart or current_x != xstart:
		current_pipe = parsed_input[current_y, current_x]
		direction = direction_switches[current_pipe, direction]
		change = increments[direction]
		loop_locations.add( (2*current_y + change[0], 2*current_x + change[1]) )
		loop_locations.add( (2*current_y + 2*change[0], 2*current_x + 2*change[1]) )
		current_y += change[0]
		current_x += change[1]
		num_steps += 1
	
	return num_steps // 2

def part2(parsed_input):
	shape = parsed_input.shape
	empty_cells = set((y,x) for (y,x) in it.product(range(-2, 2*shape[0]+2), range(-2, 2*shape[1]+2)) if (y,x) not in loop_locations)
	graph = nx.Graph()
	for cell in empty_cells:
		graph.add_node(cell)
		left_nb, top_nb, right_nb, bottom_nb = (tuple(map(sum, zip(cell, increments[i]))) for i in range(4))
		if left_nb in empty_cells:
			graph.add_edge(cell, left_nb)
		if top_nb in empty_cells:
			graph.add_edge(cell, top_nb)
		if right_nb in empty_cells:
			graph.add_edge(cell, right_nb)
		if bottom_nb in empty_cells:
			graph.add_edge(cell, bottom_nb)
	vertices = graph.nodes
	outside_cells = nx.node_connected_component(graph, (-1,-1))
	num_inside_cells = len([(x // 2, y // 2) for (x,y) in vertices if x % 2 == 0 and y % 2 == 0 and (x,y) not in outside_cells])
	return num_inside_cells

if __name__ == "__main__":
	global direction_switches
	global increments
	global loop_locations

	direction_switches = {
		('|', 1): 1, ('|', 3): 3, \
		('-', 0): 0, ('-', 2): 2, \
		('L', 3): 2, ('L', 0): 1, \
		('J', 2): 1, ('J', 3): 0, \
		('7', 2): 3, ('7', 1): 0, \
		('F', 1): 2, ('F', 0): 3
	}
	increments = {0: (0, -1), 1: (-1, 0), 2: (0, 1), 3:(1, 0)}

	loop_locations = set()

	for filename in sys.argv[1:]:
		print(f'Filename: {filename}')
		parsed_input = parse(filename)

		# Solving today's puzzles
		print(f'Part one: {part1(parsed_input)}')
		print(f'Part two: {part2(parsed_input)}')
