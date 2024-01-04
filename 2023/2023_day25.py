# Python file for solving the puzzles of day 25 of Advent of Code 2023
import itertools as it
import numpy as np
import sys
import re
import networkx as nx
from math import inf

def parse(puzzle_input):
	'''Method for parsing the puzzle input into a more suitable format for computations'''
	with open(puzzle_input, 'r+') as f:
		parsed_input = {}
		for line in f.readlines():
			vtx, neighbours = line.strip().split(': ')
			neighbours = neighbours.split()
			parsed_input[vtx] = neighbours
	return parsed_input

def part1(parsed_input):
	graph = nx.Graph()
	first = True
	s = None
	for vtx in parsed_input:
		if first:
			s = vtx
			first = False
		for nb in parsed_input[vtx]:
			graph.add_edge(vtx, nb, capacity=1.0)
	
	print(s)
	min_cut = None
	min_cut_value = inf
	for t in parsed_input:
		if s == t:
			continue
		else:
			print(t)
			cut_value, partition = nx.minimum_cut(graph, s, t)
			if cut_value < min_cut_value:
				min_cut_value = cut_value
				min_cut = partition
	print(min_cut)
	return len(min_cut[0]) * len(min_cut[1])

def part2(parsed_input):
	pass

if __name__ == "__main__":
	for filename in sys.argv[1:]:
		print(f'Filename: {filename}')
		parsed_input = parse(filename)

		# Solving today's puzzles
		print(f'Part one: {part1(parsed_input)}')
		print(f'Part two: {part2(parsed_input)}')
