# Python file for solving the puzzles of day 20 of Advent of Code 2023
import itertools as it
import numpy as np
import sys
import re
from collections import deque
from math import gcd

def parse(puzzle_input):
	'''Method for parsing the puzzle input into a more suitable format for computations'''
	with open(puzzle_input, 'r+') as f:
		parsed_input = list(map(str.strip, f.readlines()))

	modules = {}
	flipflops_modules = set()
	conjunction_modules = set()
	for line in parsed_input:
		name, destinations_list = line.split(' -> ')
		destinations_list = destinations_list.split(', ')
		type = 'b%&'.index(name[0])

		if type == 0:
			# Broadcasters
			modules['broadcaster'] = {'destinations': destinations_list}
		elif type == 1:
			# Flip-flop modules
			modules[name[1:]] = {'state': 0, 'destinations': destinations_list}
			flipflops_modules.add(name[1:])
		else:
			# Conjunction modules
			modules[name[1:]] = {'last_pulses': {}, 'destinations': destinations_list}
			conjunction_modules.add(name[1:])
	
	modules['button'] = {'destinations': ['broadcaster']}

	for name in modules:
		for nb in modules[name]['destinations']:
			if nb in conjunction_modules:
				modules[nb]['last_pulses'][name] = 0
	return modules, flipflops_modules, conjunction_modules

def part1(modules, flipflops_modules, conjunction_modules):
	iter = 1
	NUM_ITERATIONS = 1_000
	num_low_pulses = 0
	num_high_pulses = 0
	while iter <= NUM_ITERATIONS:
		# print(f'Iteration {iter}')
		queue = deque()
		queue.append((0, 'button', 'broadcaster'))
		while queue:
			pulse, src, dst = queue.popleft()
			if pulse:
				# print(f'{src} -high-> {dst}')
				num_high_pulses += 1
			else:
				# print(f'{src} -low-> {dst}')
				num_low_pulses += 1

			if dst == 'broadcaster':
				# Broadcast button pulse to broadcaster's neighbours
				for nb in modules['broadcaster']['destinations']:
					queue.append((pulse, 'broadcaster', nb))

			elif dst in flipflops_modules:
				if pulse == 0:
					modules[dst]['state'] = 1 - modules[dst]['state']
					for nb in modules[dst]['destinations']:
						queue.append((modules[dst]['state'], dst, nb))
			elif dst in conjunction_modules:
				# dst in conjunction_modules
				modules[dst]['last_pulses'][src] = pulse
				if sum(modules[dst]['last_pulses'][idx] for idx in modules[dst]['last_pulses']) \
					== len(modules[dst]['last_pulses']):
					for nb in modules[dst]['destinations']:
						queue.append((0, dst, nb))
				else:
					for nb in modules[dst]['destinations']:
						queue.append((1, dst, nb))
			else:
				pass
		iter += 1
	
	return num_high_pulses * num_low_pulses
	
def part2(modules, flipflops_modules, conjunction_modules):
	lengths = {}
	visited = {
		name: 0 for name in modules if 'jq' in modules[name]['destinations']
	}
	iter = 1
	while True:
		queue = deque()
		queue.append((0, 'button', 'broadcaster'))
		while queue:
			pulse, src, dst = queue.popleft()
			if dst == 'jq' and pulse == 1:
				visited[src] += 1
				if src not in lengths:
					lengths[src] = iter
				
				if min(visited.values()) >= 1:
					result = 1
					for length in lengths.values():
						result = (result * length) // gcd(result, length)
					return result
			
			if dst == 'broadcaster':
				# Broadcast button pulse to broadcaster's neighbours
				for nb in modules['broadcaster']['destinations']:
					queue.append((pulse, 'broadcaster', nb))

			elif dst in flipflops_modules:
				if pulse == 0:
					modules[dst]['state'] = 1 - modules[dst]['state']
					for nb in modules[dst]['destinations']:
						queue.append((modules[dst]['state'], dst, nb))
			elif dst in conjunction_modules:
				# dst in conjunction_modules
				modules[dst]['last_pulses'][src] = pulse
				if sum(modules[dst]['last_pulses'][idx] for idx in modules[dst]['last_pulses']) \
					== len(modules[dst]['last_pulses']):
					for nb in modules[dst]['destinations']:
						queue.append((0, dst, nb))
				else:
					for nb in modules[dst]['destinations']:
						queue.append((1, dst, nb))
			else:
				pass
		iter += 1
	
if __name__ == "__main__":
	for filename in sys.argv[1:]:
		print(f'Filename: {filename}')

		# Solving today's puzzles
		modules, flipflops_modules, conjunction_modules = parse(filename)
		print(f'Part one: {part1(modules, flipflops_modules, conjunction_modules)}')

		modules, flipflops_modules, conjunction_modules = parse(filename)
		print(f'Part two: {part2(modules, flipflops_modules, conjunction_modules)}')
