# Python file for solving the puzzles of day 5 of Advent of Code 2023
import sys
from math import inf

def determine_mapping_value(maps, num, type):
	for dst_start, src_start, range_length in maps[type]['tuples']:
		if src_start <= num < src_start + range_length:
			return dst_start + (num - src_start)
	return num


def parse(puzzle_input):
	'''Method for parsing the puzzle input into a more suitable format for computations'''
	with open(puzzle_input, 'r+') as f:
		inp = list(map(str.strip, f.readlines()))
		parsed_input = []
		current_part = []
		for line in inp:
			if line == '':
				parsed_input.append(current_part)
				current_part = []
			else:
				current_part.append(line)
		parsed_input.append(current_part)
	return parsed_input

def part1(parsed_input):
	maps = {}
	type = 0
	for line in parsed_input:
		if line[0].startswith('seeds'):
			seeds = list(map(int, line[0].split(': ')[1].split(' ')))
		elif 'map' in line[0]:
			maps[type] = {'tuples': []}
			for j in range(1, len(line)):
				maps[type]['tuples'].append( tuple(int(i) for i in line[j].split()) )
		type += 1

	# Seed -> soil -> fertilizer -> water -> light -> temperature -> humidity -> location
	min_location = inf
	for s in seeds:
		for t in range(1, type):
			s = determine_mapping_value(maps, s, t)
		if s < min_location:
			min_location = s
	return min_location


def determine_subranges(ranges, maps, type):
	subranges = []
	for (start, end) in ranges:
		start_idx = start
		while start_idx < end:
			added_range = False
			for dst_start, src_start, length in maps[type]['tuples']:
				src_end = src_start + length
				if src_start <= start_idx < src_end:
					shift = dst_start - src_start
					range_start = start_idx + shift
					range_end = min(end + shift, src_end + shift)
					subranges.append((range_start, range_end))
					start_idx += range_end - range_start
					added_range = True
					break

			if not added_range:
				# find smallest larger src_start
				remaining_startids = list(filter(lambda x: x[1] > start_idx, maps[type]['tuples']))
				if len(remaining_startids):
					new_start = min(remaining_startids, key = lambda x: x[1])[1]

					subranges.append((start_idx, new_start))
					start_idx = new_start
				else:
					# There exists no nontrivial mapping, so values are mapped to themselves
					subranges.append((start_idx, end))
					start_idx = end
	return subranges

def part2(parsed_input):
	maps = {}
	type = 0
	for line in parsed_input:
		if line[0].startswith('seeds'):
			seed_ranges = list(map(int, line[0].split(': ')[1].split(' ')))
		elif 'map' in line[0]:
			maps[type] = {'tuples': []}
			for j in range(1, len(line)):
				maps[type]['tuples'].append( tuple(int(i) for i in line[j].split()) )
		type += 1


	ranges = list(
			(seed_ranges[2*idx], seed_ranges[2*idx] + seed_ranges[2*idx+1]) \
			for idx in range(len(seed_ranges) // 2)
	)

	for t in range(1, type):
		ranges = determine_subranges(ranges, maps, t)
	return min(r[0] for r in ranges)

if __name__ == "__main__":
	for filename in sys.argv[1:]:
		print(f'Filename: {filename}')
		parsed_input = parse(filename)

		# Solving today's puzzles
		print(f'Part one: {part1(parsed_input)}')
		print(f'Part two: {part2(parsed_input)}')
