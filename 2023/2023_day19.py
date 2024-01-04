# Python file for solving the puzzles of day 19 of Advent of Code 2023
from functools import reduce
import itertools as it
import numpy as np
import sys
import re

def process_workflow(workflows, name, variable_mapping, x, m, a, s):
	for instr in workflows[name]:
		if ':' not in instr:
			# Last statement
			if instr == 'A':
				return x + m + a + s
			elif instr == 'R':
				return 0
			else:
				return process_workflow(workflows, instr, variable_mapping, x, m, a, s)

		variable, sign, val = re.search('([xmas])([<>])(\d+)', instr).groups()
		variable = variable_mapping[variable]
		val = int(val)
		goto = instr.split(':')[-1]
		if sign == '<':
			if variable < val:
				if goto == 'A':
					return x + m + a + s
				elif goto == 'R':
					return 0
				else:
					return process_workflow(workflows, goto, variable_mapping, x, m, a, s)
		else:
			if variable > val:
				if goto == 'A':
					return x + m + a + s
				elif goto == 'R':
					return 0
				else:
					return process_workflow(workflows, goto, variable_mapping, x, m, a, s)

def find_combinations(workflows):
	letters = 'xmas'
	acceptance_score = 0
	bounds = {k : [1, 4000] for k in letters}
	queue = [('in', 0, bounds)]

	while len(queue):
		# print(queue)
		name, instr_id, bounds = queue.pop(0)

		if instr_id < len(workflows[name]) - 1:
			# Not the last instruction in the workflow
			instr = workflows[name][instr_id]
			variable, sign, val = re.search('([xmas])([<>])(\d+)', instr).groups()
			val = int(val)
			goto = instr.split(':')[-1]

			lb, ub = bounds[variable]
			assert lb <= ub

			new_bounds_first = bounds.copy()
			new_bounds_second = bounds.copy()
			if sign == '<':
				new_bounds_first[variable] = [lb, val - 1]
				new_bounds_second[variable] = [val, ub]
			else:
				new_bounds_first[variable] = [val + 1, ub]
				new_bounds_second[variable] = [lb, val]

			if new_bounds_first[variable][0] <= new_bounds_first[variable][1]:
				if goto == 'A':
					val = reduce(lambda x, y: x * y, (new_bounds_first[k][1] - new_bounds_first[k][0] + 1 for k in new_bounds_first))
					print(val, new_bounds_first)
					acceptance_score += val
				elif goto == 'R':
					acceptance_score += 0
				else:
					queue.append( (goto, 0, new_bounds_first) )
					# print(queue)

			if new_bounds_second[variable][0] <= new_bounds_second[variable][1]:
				queue.append( (name, instr_id + 1, new_bounds_second) )
				# print(queue)

		else:
			# Last instruction of workflow
			instr = workflows[name][instr_id]
			if instr == 'A':
				acceptance_score += reduce(lambda x, y: x * y, (bounds[k][1] - bounds[k][0] + 1 for k in bounds))
			elif instr == 'R':
				acceptance_score += 0
			else:
				queue.append( (instr, 0, bounds) )
	return acceptance_score

def parse(puzzle_input):
	'''Method for parsing the puzzle input into a more suitable format for computations'''
	with open(puzzle_input, 'r+') as f:
		workflows, part_ratings = {}, []
		is_workflow = True
		for line in f.readlines():
			if line == '\n':
				is_workflow = False
			else:
				if is_workflow:
					# Parse workflow
					x = re.search('(\w+)\{(.*)\}', line)
					name, workflow = x.groups()
					workflow = workflow.split(',')
					workflows[name] = workflow
				else:
					part_ratings.append(line.strip())

	return workflows, part_ratings

def part1(workflows, part_ratings):
	score = 0
	for rating in part_ratings:
		x, m, a, s = (int(i) for i in re.findall('\d+', rating))
		variable_mapping = {'x': x, 'm': m, 'a': a, 's': s}
		score += process_workflow(workflows, 'in', variable_mapping, x, m, a, s)
	return score

def part2(workflows):
	return find_combinations(workflows)

if __name__ == "__main__":	
	global acceptance_score
	acceptance_score = 0
	for filename in sys.argv[1:]:
		print(f'Filename: {filename}')
		workflows, part_ratings = parse(filename)

		# Solving today's puzzles
		print(f'Part one: {part1(workflows, part_ratings)}')
		print(f'Part two: {part2(workflows)}')
