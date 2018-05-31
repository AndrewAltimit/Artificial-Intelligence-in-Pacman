# Overview
Pacman search agent implemented in Python.

## Features
* Breadth-First Search
* Depth-First Search
* A\* Search
* Adjustable Cost Function
* Unit Testing and Benchmarking


## Prerequisites
Python 2.7.* https://www.python.org/download/releases/2.7/
 

## Usage

***Initializing Script***

	python pacman.py
	
***Finding a Fixed Food Dot using Search Algorithms***

	python pacman.py -l tinyMaze -p SearchAgent -a fn=tinyMazeSearch
	
***Varying the Cost Function***

	python pacman.py -l mediumMaze -p SearchAgent -a fn=ucs
	
***Finding All the Corners***

	python pacman.py -l mediumCorners -p AStarCornersAgent -z 0.5
	
	
***Eating All The Dots***
	
	python pacman.py -l testSearch -p AStarFoodSearchAgent
	
***Greedy Agent***
	
	python pacman.py -l bigSearch -p ClosestDotSearchAgent -z .5 

## Unit Testing and Benchmarking

***Full Test***

	python autograder.py
	
***Single Test***

	python autograder.py -q q2
