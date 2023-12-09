# Python file for solving the puzzles of day 7 of Advent of Code 2023
import itertools as it
import numpy as np
import sys
import re
from collections import Counter

def determine_hand_score(hand, part_one):
	unique_cards = Counter(hand)
	if len(unique_cards) == 1:
		return 7
	
	if not part_one:
		val_j = unique_cards['J']
		del unique_cards['J']
		most_common = unique_cards.most_common(1)
		print(f'Most common: {hand, most_common}')
		unique_cards[most_common[0][0]] += val_j
		print(unique_cards)

	max_value = max(unique_cards.values())
	min_value = min(unique_cards.values())


	# Decision tree
	if max_value == 5:
		return 7
	elif max_value == 4:
		return 6
	elif max_value == 3:
		if min_value == 2:
			return 5
		else:
			return 4
	elif max_value == 2:
		if len(unique_cards) == 3:
			return 3
		else:
			return 2
	else:
		return 1


def parse(puzzle_input):
	'''Method for parsing the puzzle input into a more suitable format for computations'''
	with open(puzzle_input, 'r+') as f:
		parsed_input = []
		for line in f.readlines():
			hand, bid = line.strip().split()
			parsed_input.append( (hand, int(bid)) )
	print(parsed_input)
	return parsed_input

def part1(parsed_input, card_values):
	hand_representations = []
	for (hand, bid) in parsed_input:
		value = 0
		for c in hand:
			value += card_values[c]
			value *= 1_000
		hand_representations.append(value)
	hand_representations = np.array(hand_representations)
	bids = np.array([line[1] for line in parsed_input])
	scores = np.array([determine_hand_score(hand, True) for (hand, bid) in parsed_input])
	indices = np.lexsort((hand_representations, scores))

	print(hand_representations, scores)
	for x in range(len(indices)):
		print(parsed_input[indices[x]])
	return sum((x+1) * bids[indices[x]] for x in range(len(indices)))



def part2(parsed_input, card_values):
	hand_representations = []
	for (hand, bid) in parsed_input:
		value = 0
		for c in hand:
			value += card_values[c]
			value *= 1_000
		hand_representations.append(value)
	hand_representations = np.array(hand_representations)
	bids = np.array([line[1] for line in parsed_input])
	scores = np.array([determine_hand_score(hand, False) for (hand, bid) in parsed_input])
	indices = np.lexsort((hand_representations, scores))

	print(hand_representations, bids, scores, indices)
	for x in range(len(indices)):
		print(x+1, parsed_input[indices[x]])

	return sum((x+1) * bids[indices[x]] for x in range(len(indices)))


if __name__ == "__main__":

	for filename in sys.argv[1:]:
		print(f'Filename: {filename}')
		parsed_input = parse(filename)

		card_values = {str(i) : i for i in range(2, 10)}
		card_values['T'] = 10
		card_values['J'] = 11
		card_values['Q'] = 12
		card_values['K'] = 13
		card_values['A'] = 14

		# Solving today's puzzles
		print(f'Part one: {part1(parsed_input, card_values)}')
	
		card_values['J'] = 1

		print(f'Part two: {part2(parsed_input, card_values)}')
