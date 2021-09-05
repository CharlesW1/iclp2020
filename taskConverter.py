import math, sys

def skyConvert(task):
	x = task.split("/")
	size = int(len(x)/4)
	x = [[k if k!= '' else '_' for k in x[i:i+size]] for i in range(0, size*4, size)]
	return "\n".join([str(size)] + [" ".join(i) for i in x]) + "\n"

def aquaConvert(task):
	x = task.split(";")
	clues = x[0].split('_')
	size = int(len(clues)/2)
	clues = [clues[i: i + size] for i in range(0, size*2, size)]
	board = x[1].split(",")
	board = [board[i: i + size] for i in range(0, size*size, size)]
	return "\n".join([str(size)] + [" ".join(i) for i in clues] + [" ".join(i) for i in board]) + "\n"

def masyuConvert(task):
	count = 0
	white = []
	black = []
	for i in task:
		if i == "B":
			black.append(count)
		if i == "W":
			white.append(count)
		count += ord(i) - ord('a') + 1 if ord(i) > ord('Z') else 1
	size = int(math.sqrt(count))
	white = ["{0} {1}".format(int(i/size), int(i%size)) for i in white]
	black = ["{0} {1}".format(int(i/size), int(i%size)) for i in black]
	return "\n".join(["{0} {1} {2}".format(size, len(white), len(black))] + white + black)

if len(sys.argv) == 1:
	print('''
	This program converts the task variable in the script section of $('#rel') on the puzzle-aquarium.com website to our desired input:\n
	\t1. a Skyscraper Puzzle Task Converter ('1', 'S', 'sky', 'skyscraper')\n
	\t2. a Aquarium Puzzle Task Converter ('2', 'A', 'aqua', 'aquarium')\n
	\t3. a Masyu Puzzle Task Converter ('3', 'M', 'mas', 'masyu')\n
	Please enter one of the quoted strings (without the \') to designate the desired converter.\n
	This program uses task.txt for input and outputs to the default input text file for the secified solver.
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
		exit()

	with open("task.txt", "r") as f:
		task = f.readline()[:-1]

	# skyscraper case
	if which == 1:
		input = skyConvert(task)
		print(input)
		with open("input.txt", "w") as f:
			f.write(input)

	# aquarium case
	if which == 2:
		input = aquaConvert(task)
		print(input)
		with open("input2.txt", "w") as f:
			f.write(input)

	# masy case
	if which == 3:
		input = masyuConvert(task)
		print(input)
		with open("input3.txt", "w") as f:
			f.write(input)
