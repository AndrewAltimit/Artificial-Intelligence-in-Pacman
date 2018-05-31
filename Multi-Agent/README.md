# Overview
Multi-agent Pacman implementation in Python.

## Features
* Alpha-Beta
* Minimax
* Expectimax


## Prerequisites
Python 2.7.* https://www.python.org/download/releases/2.7/
 

## Usage

***Initializing Script***

	python pacman.py
	
***Alpha-Beta Agent***

	python pacman.py -p AlphaBetaAgent -a depth=3 -l smallClassic
	
***Minimax Agent***

	python pacman.py -p MinimaxAgent -l minimaxClassic -a depth=4
	
***Expectimax Agent***

	python pacman.py -l smallClassic -p ExpectimaxAgent -a evalFn=better -q -n 10
	

## Unit Testing and Benchmarking

***Full Test***

	python autograder.py
	
***Single Test***

	python autograder.py -q q2
