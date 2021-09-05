# iclp2020contest

This is Charles Weng's Final Project for Stony Brook University's Annie Liu's CSE 526 Spring 2021 section. The project was inspired by the ICLP 2020 Contest and utilizes constraints to solve the Skyscraper and Aquarium Puzzle.

This project is dependent on Python and the external module Clingo, which implements constraint functionalities into Python.

Version of Python used during development was 3.6.1.

Version of Clingo used during development was 5.5.0.


driver.py contains the interface and the two solvers.

Skyscraper requires a text file with the following specifications:

		1. First line contains the board size (for an 8x8 board, put 8)

		2. Second line contains the column clues in order from the top

		3. Third line contains the column clues in order from the bottom

		4. Fourth line contains the row clues in order from the left

		5. Fifth line contains the row clues in order from the right



Aquarium puzzle requires a text file with the following specifications:

		1. First line contains the board size (for an NxN board, put N)

		2. Second line contains the column clues in order

		4. Third line contains the row clues in order

		5. Next N lines describes which tank each space belongs to



Masyu puzzle requires a text file with the following specifications:

		1. First line contains the board size minus one, the number of white circles, and the number of black circles

		2. The following lines contain the coordinates of the circles (white first) (0 indexed; formated as 'x y')



The first puzzles support _ in place of an empty clue.

ExtraTests folder contains tests cases and some graphs of the runtime.
