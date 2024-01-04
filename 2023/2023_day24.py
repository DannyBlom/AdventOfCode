# Python file for solving the puzzles of day 24 of Advent of Code 2023
import itertools as it
import numpy as np
import sympy as sp
import sys
import re

def compute_ray_intersection(hailstones, a, b, min_axis, max_axis):
	ax, ay, az, adx, ady, adz = hailstones[a].values()
	bx, by, bz, bdx, bdy, bdz = hailstones[b].values()

	# The question is whether there exists nonnegative u, v such that
	# ax + u * adx == bx + v * bdx 
	# ay + u * ady == by + v * bdy

	# Multiplying the first with bdy and the second with bdx gives
	# ax * bdy + u * adx * bdy == bx * bdy + v * bdx * bdy
	# ay * bdx + u * ady * bdx == by * bdx + v * bdy * bdx	-
	# -------------------------------------------------------
	# (ax * bdy - ay * bdx) + u * (adx * bdy - ady * bdx) == bx * bdy - by * bdx 

	if (adx * bdy - ady * bdx) != 0:
		u = 1.0 * (bx * bdy - by * bdx - (ax * bdy - ay * bdx)) / (adx * bdy - ady * bdx)
		v = (ax + u * adx - bx) / bdx
	
		if u >= 0 and v >= 0 and min_axis <= ax + u * adx <= max_axis and min_axis <= ay + u * ady <= max_axis:
			return True
	return False
			
def parse(puzzle_input):
	'''Method for parsing the puzzle input into a more suitable format for computations'''
	with open(puzzle_input, 'r+') as f:
		hailstones = {}
		for idx, line in enumerate(f.readlines()):
			data = line.strip().split('@')
			x, y, z = (int(i) for i in data[0].split(', '))
			dx, dy, dz = (int(i) for i in data[1].split(', '))
			hailstones[idx] = {'x': x, 'y': y, 'z': z, 'dx': dx, 'dy': dy, 'dz': dz}
	return hailstones

def part1(hailstones):
	min_axis = 200000000000000
	max_axis = 400000000000000
	score = 0

	for (a, b) in it.combinations(hailstones, r=2):
		# Determine intersection point if it exists
		score += compute_ray_intersection(hailstones, a, b, min_axis, max_axis)
	return score

def equations(vars):
	

	print(fx, fy, fz, fdx, fdy, fdz )
	x, y, z, dx, dy, dz, t, u, v = vars

	eq1 = fx - x + t*(fdx - dx)
	eq2 = fy - y + t*(fdy - dy)
	eq3 = fz - z + t*(fdz - dz)
	eq4 = sx - x + u*(sdx - dx)
	eq5 = sy - y + u*(sdy - dy)
	eq6 = sz - z + u*(sdz - dz)
	eq7 = tx - x + v*(tdx - dx)
	eq8 = ty - y + v*(tdy - dy)
	eq9 = tz - z + v*(tdz - dz)

	return [eq1, eq2, eq3, eq4, eq5, eq6, eq7, eq8, eq9]


def part2(hailstones):
	# We have six unknowns, namely xr, yr, zr, rdx, rdy, rdz of location and velocity of the throw
	# Furthermore, given hailstones a and b, with velocities (adx - rdx, ady - rdy, adz - rdz) and 
	# (bdx - rdx, bdy - rdy, bdz - rdz) should hit the same point
	first = hailstones[0]
	second = hailstones[1]
	third = hailstones[2]

	unknowns = sp.symbols('x y z dx dy dz t u v')
	x, y, z, dx, dy, dz, t, u, v = unknowns
	
	equations = []
	for time, hailstone in zip([t,u,v], [first, second, third]):
		hvalues = list(hailstone.values())
		equations.append(sp.Eq(x + time * dx, hvalues[0] + time * hvalues[3]))
		equations.append(sp.Eq(y + time * dy, hvalues[1] + time * hvalues[4]))
		equations.append(sp.Eq(z + time * dz, hvalues[2] + time * hvalues[5]))
	solution = sp.solve(equations, unknowns)
	return sum(solution[0][:3])

if __name__ == "__main__":
	global hailstones
	for filename in sys.argv[1:]:
		print(f'Filename: {filename}')
		hailstones = parse(filename)

		# Solving today's puzzles
		print(f'Part one: {part1(hailstones)}')
		print(f'Part two: {part2(hailstones)}')
