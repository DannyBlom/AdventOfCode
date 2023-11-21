for i in range(1, 26):
	with open(f'2023_day{i}.py', 'w+') as f:
		f.write(f"# Python file for solving the puzzles of day {i} of Advent of Code 2023\n")
		f.write("import itertools as it\nimport numpy as np\nimport sys\nimport re\n\n")
		f.write("def parse(puzzle_input):\n")
		f.write("\t'''Method for parsing the puzzle input into a more suitable format for computations'''\n")
		f.write("\tparsed_input = list(map(str.strip, puzzle_input.readlines()))\n")
		f.write("\treturn parsed_input\n\n")
		f.write("def part1(parsed_input):\n\tpass\n\n")
		f.write("def part2(parsed_input):\n\tpass\n\n")
		f.write('if __name__ == "__main__":\n')
		f.write("\tfor filename in sys.argv[1:]:\n")
		f.write("\t\tprint(f'Filename: {filename}')\n")
		f.write("\t\tparsed_input = parse(filename)\n\n")
		f.write("\t\t# Solving today's puzzles\n")
		f.write("\t\tprint(f'Part one: {part1(parsed_input)}')\n")
		f.write("\t\tprint(f'Part two: {part2(parsed_input)}')\n")