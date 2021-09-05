import clingo
import sys
import random
import time

# helper function to check if clue exists
def clueExists(str):
	if str == "_":
		return '0'
	return str

def skyClues(l):
	listt = l.copy()
	left, max = 0, 0
	for i in listt:
		if i > max:
			max = i
			left += 1
	listt.reverse()
	right, max = 0, 0
	for i in listt:
		if i > max:
			max = i
			right += 1
	return [left, right]

def skyComp(given, generated):
	if given[0] != '_' and int(given[0]) != generated[0]:
		return False
	if given[1] != '_' and int(given[1]) != generated[1]:
		return False
	return True

def Skyscraper(filename):

	############################################################################
	# 	Parse file
	############################################################################

	with open(filename, "r") as f:
		content = f.readlines()
		content = [x.strip().split() for x in content]

	# capture board size
	n = int(content[0][0])

	# capture row and col clues
	colClues = [[content[1][x], content[2][x]] for x in range(n)]
	rowClues = [[content[3][x], content[4][x]] for x in range(n)]


	############################################################################
	# 	Board Rules
	############################################################################

	# size of board
	board =  "#const n = {0}.\n".format(n)

	# can only one building height on each spot
	board += "{build(X,Y,1..n)} = 1 :- X=1..n, Y=1..n.\n"

	# each row and column has unique building height
	board += ":- build(X,Y,K), build(X,B,K), Y!=B.\n"
	board += ":- build(X,Y,K), build(A,Y,K), X!=A.\n\n"


	############################################################################
	# 	Clue Constraint Rules
	############################################################################

	# prop(row/col, index, clue, max)
	# 		row/col - which row/col are we doing the propagtion check for
	#		index - index inside of row/col
	#		clue - how clue changes as we pass by buildings
	#		max - current max height seen
	#		endstate should always be a clue of 1 and a max height seen of n

	# propagation endstate value
	constraints =  "down(1..n,n,1,n).\n"
	constraints += "up(1..n,1,1,n).\n"
	constraints += "right(1..n,n,1,n).\n"
	constraints += "left(1..n,1,1,n).\n"

	# propagation can only have a unique value for clue and max
	constraints += ":- down(X,Y, A, B), down(X,Y, A, D), D != B.\n"
	constraints += ":- down(X,Y, A, B), down(X,Y, C, B), A != C.\n"

	constraints += ":- up(X,Y, A, B), up(X,Y, A, D), D != B.\n"
	constraints += ":- up(X,Y, A, B), up(X,Y, C, B), A != C.\n"

	constraints += ":- right(X, Y, A, B), right(X, Y, A, D), D != B.\n"
	constraints += ":- right(X, Y, A, B), right(X, Y, C, B), A != C.\n"

	constraints += ":- left(X,Y, A, B), left(X,Y, A, D), D != B.\n"
	constraints += ":- left(X,Y, A, B), left(X,Y, C, B), A != C.\n"

	# propagation rules (how the states change as you propagte)
	constraints += "down(X, ROW + 1, CLUE, MAX) :- down(X, ROW, CLUE, MAX), build(ROW + 1, X, H), H < MAX.\n"
	constraints += "down(X, ROW + 1, CLUE - 1, H) :- down(X, ROW, CLUE, MAX), build(ROW + 1, X, H), H > MAX.\n"

	constraints += "up(X, ROW - 1, CLUE, MAX) :- up(X, ROW, CLUE, MAX), build(ROW - 1, X, H), H < MAX.\n"
	constraints += "up(X, ROW - 1, CLUE - 1, H) :- up(X, ROW, CLUE, MAX), build(ROW - 1, X, H), H > MAX.\n"

	constraints += "right(X, COL + 1, CLUE, MAX) :- right(X, COL, CLUE, MAX), build(X, COL + 1, H), H < MAX.\n"
	constraints += "right(X, COL + 1, CLUE - 1, H) :- right(X, COL, CLUE, MAX), build(X, COL + 1, H), H > MAX.\n"

	constraints += "left(X, COL - 1, CLUE, MAX) :- left(X, COL, CLUE, MAX), build(X, COL - 1, H), H < MAX.\n"
	constraints += "left(X, COL - 1, CLUE - 1, H) :- left(X, COL, CLUE, MAX), build(X, COL - 1, H), H > MAX.\n"


	############################################################################
	# 	Clues
	############################################################################

	# input given clues (clue is 0 if missing)
	clues =  "".join(["colClue({0}, {1}, {2}).\n".format(i, clueExists(colClues[i-1][0]), clueExists(colClues[i-1][1])) for i in range(1, n+1)])
	clues += "".join(["rowClue({0}, {1}, {2}).\n".format(i, clueExists(rowClues[i-1][0]), clueExists(rowClues[i-1][1])) for i in range(1, n+1)])

	# define propagation start (clue = 0 if missing)
	clues += "down(X, 1, CLUE1, H) :- colClue(X, CLUE1, CLUE2), build(1,X,H), CLUE1 != 0.\n"
	clues += "up(X, n, CLUE2, H) :- colClue(X, CLUE1, CLUE2), build(n,X,H), CLUE2 != 0.\n"
	clues += "right(X, 1, CLUE1, H) :- rowClue(X, CLUE1, CLUE2), build(X,1,H), CLUE1 != 0.\n"
	clues += "left(X, n, CLUE2, H) :- rowClue(X, CLUE1, CLUE2), build(X,n,H), CLUE2 != 0.\n"


	############################################################################
	# 	Export generated constraints
	############################################################################

	# output generated constraints into a file
	# with open("test.txt", "w") as f:
	# 	f.write(board)
	# 	f.write(constraints)
	# 	f.write(clues)


	############################################################################
	# 	Use Clingo to Solve
	############################################################################

	# add constraints and solve
	ctl = clingo.Control()
	ctl.add("base", [], board + constraints + clues +"#show build/3.")
	ctl.ground([("base", [])])
	sol = ctl.solve(yield_=True)


	############################################################################
	# 	Organize Solution
	############################################################################

	# process model
	model = sol.model()
	matrix = [[0]*n for i in range(n)]

	# no solutions
	if model is None:
		print("No solutions found")
		return

	# model gives matrix entries in random order
	for entry in str(model).split():
		if entry[:5] == "build":
			building = [int(x) for x in entry[6:-1].split(",")]
			matrix[building[0]-1][building[1]-1] = building[2]

	# further process into printable result
	ans = "\n".join([" ".join([str(x) for x in row]) for row in matrix])

	# ensure clues check
	for i in range(0,n):
		if not comp(rowClues[i], skyClues(matrix[i])):
			print("row clue check failed for row {0}".format(i))
		transpose = [[matrix[y][x] for y in range(0,n)] for x in range(0,n)]
		if not comp(colClues[i], skyClues(transpose[i])):
			print("col clue check failed for col {0}".format(i))

	# save output to output.text
	print(ans)
	with open("output.txt", "w") as f:
		f.write(ans + "\n")
	# print(sol.model())

	return ans


def Aquarium(filename):

	############################################################################
	# 	Parse file
	############################################################################

	with open(filename, "r") as f:
		content = f.readlines()
		content = [x.strip().split() for x in content]

	# capture board size
	n = int(content[0][0])

	# capture row and column clues
	colClues = [content[1][x] for x in range(n)]
	rowClues = [content[2][x] for x in range(n)]

	# capture tank states into matrix
	tanks = [content[x] for x in range(3, 3+n)]

	# integrity check on tanks size
	if any([len(tanks)-n for row in tanks]):
		print("Bad tank input")
		return


	############################################################################
	# 	Board Rules
	############################################################################

	# size of board
	board = "#const n = {0}.\n".format(n)

	# input tanks
	board += "".join(["tanks({0}, {1}, {2}).\n".format(x, y, tanks[x][y]) for x in range(n) for y in range(n)])

	# each tank needs a fill value
	board += "{filled(X, Y, 0..1)} = 1 :- tanks(X,Y,T).\n"


	############################################################################
	# 	Clue Constraint Rules
	############################################################################

	# tank T is filled up to Y
	constraints = "tank(T,X) :- tanks(X,Y,T), filled(X,Y,1).\n"

	# if tank T is filled up to Y, then fill other spaces in tank
	constraints += "filled(X2,Y,1) :- tank(T, X), tanks(X2, Y, T), X <= X2.\n"

	# cannot be filled and not filled
	constraints += ":- filled(X,Y,0), filled(X,Y,1).\n"


	############################################################################
	# 	Clues
	############################################################################

	# column clues (there are #clue number of tanks filled in column)
	clues = "".join(["{{filled(0..{1}, {0}, 1)}} = {2}.\n".format(i, n-1, colClues[i]) for i in range(n) if colClues[i] != "_"])

	# row clues (there are #clue number of tanks filled in row)
	clues += "".join(["{{filled({0}, 0..{1}, 1)}} = {2}.\n".format(i, n-1, rowClues[i]) for i in range(n) if rowClues[i] != "_"])


	############################################################################
	# 	Export generated constraints
	############################################################################

	# output generated constraints into a file
	# with open("test.txt", "w") as f:
	# 	f.write(board)
	# 	f.write(constraints)
	# 	f.write(clues)


	############################################################################
	# 	Use Clingo to Solve
	############################################################################

	# run clingo and solve
	ctl = clingo.Control()
	ctl.add("base", [], board + constraints + clues + "#show filled/3.")
	ctl.ground([("base", [])])
	sol = ctl.solve(yield_=True)


	# ############################################################################
	# 	Organize Solution
	############################################################################

	# get first solution
	model = sol.model()
	matrix = [[0]*n for i in range(n)]

	# no solutions
	if model is None:
		print("No solutions found")
		return

	# model gives matrix entries in random order
	for entry in str(model).split():
		if entry[:6] == "filled":
			fill = [int(x) for x in entry[7:-1].split(",")]
			matrix[fill[0]][fill[1]] = fill[2]

	# further process into printable result
	matrix = [["*" if x == 1 else "." for x in row] for row in matrix]
	ans = "\n".join(["".join([x for x in row]) for row in matrix])

	# ensure clues check
	sumRows = [i.count('*') for i in matrix]
	transpose = [[matrix[y][x] for y in range(0,n)] for x in range(0,n)]
	sumCols = [i.count('*') for i in transpose]
	for i in range(0, n):
		if rowClues[i] != '_' and int(rowClues[i]) != sumRows[i]:
			print("row clue check failed for row {0}".format(i))
		if colClues[i] != '_' and int(colClues[i]) != sumCols[i]:
			print("row clue check failed for row {0}".format(i))


	# print and store output
	print(ans)
	with open("output.txt", "w") as f:
		f.write(ans + "\n")
	# print(sol.model())

	return ans



def Masyu(filename):

	############################################################################
	# 	Parse file
	############################################################################

	with open(filename, "r") as f:
		content = f.readlines()
		content = [x.strip().split() for x in content]

	# capture board size
	n = int(content[0][0]) + 1


	# capture black and white tiles
	w = int(content[0][1])
	whiteClues = [(content[x][0], content[x][1]) for x in range(1, 1 + w)]
	b = int(content[0][2])
	blackClues = [(content[x][0], content[x][1]) for x in range(1 + w, 1 + w + b)]


	############################################################################
	# 	Board Rules
	############################################################################

	# size of board
	board =  "#const n = {0}.\n".format(n)

	# board
	board += "tile(0..n-1, 0..n-1).\n"


	############################################################################
	# 	Clue Constraint Rules
	############################################################################

	# edge constraints (connects adjacent; no self connect; no 2-cycle)
	constraints  = ":- edge(X,Y, A,B), |X - A| + |Y - B| > 1.\n"
	constraints += ":- edge(X,Y, X,Y).\n"
	constraints += ":- edge(X,Y, A,B), edge(A,B, X,Y).\n"

	# cycle constraints (in/out count at most 1 each; in/out parity)
	constraints += "{edge(X,Y, 0..(n-1),0..(n-1))} <= 1 :- tile(X,Y).\n"
	constraints += "{edge(0..(n-1),0..(n-1), A,B)} <= 1 :- tile(A,B).\n"
	constraints += "{edge(X,Y, 0..(n-1),0..(n-1))} = 1 :- edge(_,_, X,Y).\n"
	constraints += "{edge(0..(n-1),0..(n-1), X,Y)} = 1 :- edge(X,Y, _,_).\n"

	# 1 cycle constraint
	constraints += "reached(A,B) :- edge(X,Y, A,B), reached(X,Y).\n"
	constraints += ":- edge(_,_, A,B), not reached(A,B).\n"

	# straight and curve definition
	constraints += "straight(X,Y):- edge(A,B, X,Y), edge(X,Y, A,D), |B-D|=2.\n"
	constraints += "straight(X,Y):- edge(A,B, X,Y), edge(X,Y, C,B), |A-C|=2.\n"
	constraints += "curve(X,Y):- edge(A,B, X,Y), edge(X,Y, C,D), |A-C| - |B-D| = 0.\n"
	constraints += ":- straight(X,Y), curve(X,Y)."

	# white and black constraints (part of cycle; definitions)
	constraints += "{edge(X,Y, 0..(n-1),0..(n-1))} = 1 :- white(X,Y).\n"
	constraints += "{edge(X,Y, 0..(n-1),0..(n-1))} = 1 :- black(X,Y).\n"

	constraints += "straight(X,Y) :- white(X,Y).\n"
	constraints += ":- white(X,Y), edge(A,B, X,Y), edge(X,Y, C,D), straight(A,B), straight(C,D).\n"

	constraints += "curve(X,Y) :- black(X,Y).\n"
	constraints += "straight(A,B) :- black(X,Y), edge(A,B, X,Y).\n"
	constraints += "straight(A,B) :- black(X,Y), edge(X,Y, A,B).\n"


	############################################################################
	# 	Clues
	############################################################################

	# input given clues
	clues =  "".join(["white({0},{1}).\n".format(x, y) for x, y in whiteClues])
	clues += "".join(["black({0},{1}).\n".format(x, y) for x, y in blackClues])
	clues += "reached({0},{1}).\n".format(whiteClues[0][0], whiteClues[0][1])


	############################################################################
	# 	Export generated constraints
	############################################################################

	# output generated constraints into a file
	with open("test.txt", "w") as f:
		f.write(board)
		f.write(constraints)
		f.write(clues)


	############################################################################
	# 	Use Clingo to Solve
	############################################################################

	# run clingo and solve
	ctl = clingo.Control()
	ctl.add("base", [], board + constraints + clues + "#show edge/4.")
	ctl.ground([("base", [])])
	sol = ctl.solve(yield_=True)

	# ############################################################################
	# 	Organize Solution
	############################################################################

	# get first solution
	model = sol.model()

	# no solutions
	if model is None:
		print("No solutions found")
		return

	hori, vert = [], []

	# model gives matrix entries in random order
	for entry in str(model).split():
		if entry[:4] == "edge":
			edge = [int(x) for x in entry[5:-1].split(",")]
			tile1, tile2 = (edge[0], edge[1]), (edge[2], edge[3])
			if tile1[0] == tile2[0]:
				hori.append(tile1) if tile1[1] < tile2[1] else hori.append(tile2)
			else:
				vert.append(tile1) if tile1[0] < tile2[0] else vert.append(tile2)
	hori.sort()
	vert.sort()


	# further process into printable result
	ans =  "{0}\n".format(len(hori))
	ans += "".join(["{0} {1}\n".format(x, y) for x, y in hori])
	ans += "{0}\n".format(len(vert))
	ans += "".join(["{0} {1}\n".format(x, y) for x, y in vert])

	# print and store output
	print(ans)
	with open("output.txt", "w") as f:
		f.write(ans)
	# print(sol.model())

	return ans



if len(sys.argv) == 1:
	print('''
This program has 3 functionalities:\n
\t1. a Skyscraper Puzzle Solver ('1', 'S', 'sky', 'skyscraper')\n
\t2. a Aquarium Puzzle Solver ('2', 'A', 'aqua', 'aquarium')\n
\t3. a Masyu Puzzle Solver ('3', 'M', 'mas', 'masyu')\n
To use one of these three programs please enter one of the quoted strings (without the \') for your desired program\n
You can enter another argument to specify the target file\n
\tSkyscraper defaults to input.txt\n
\tAquarium defaults to input2.txt\n
\tMasyu defaults to input3.txt\n
Any third argument shows the runtime of the solver\n
(refer to README.md for specifications on input)
	''')

if len(sys.argv) != 1:
	# determine case
	which = sys.argv[1].strip().lower()
	case = {"skyscraper":1,
		"1": 1,
		"s": 1,
		"sky":1,
		"aquarium":2,
		"2": 2,
		"a": 2,
		"aqua":2,
		"masyu":3,
		"3": 3,
		"m": 3,
		"mas": 3,

		}
	which  = case.get(which, 0)

	# no match
	if which == 0:
		print("Please enter a valid program\nRun without arguments for more instructions")

	# skyscraper case
	if which == 1:
		file = "input.txt"
		if len(sys.argv) > 2:
			file = sys.argv[2]
		if len(sys.argv) > 3:
			start = time.time()
			Skyscraper(file)
			print(time.time() - start)
		else:
			Skyscraper(file)

	# aquarium case
	if which == 2:
		file = "input2.txt"
		if len(sys.argv) > 2:
			file = sys.argv[2]
		if len(sys.argv) > 3:
			start = time.time()
			Aquarium(file)
			print(time.time() - start)
		else:
			Aquarium(file)

	# masy case
	if which == 3:
		file = "input3.txt"
		if len(sys.argv) > 2:
			file = sys.argv[2]
		if len(sys.argv) > 3:
			start = time.time()
			Masyu(file)
			print(time.time() - start)
		else:
			Masyu(file)
