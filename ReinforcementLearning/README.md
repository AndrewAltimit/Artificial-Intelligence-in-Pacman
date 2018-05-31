# Overview
Reinforcement Learning within Pacman.

## Features
* Q-Learning
* Value Iteration (Markov Decision Process)


## Prerequisites
Python 2.7.* https://www.python.org/download/releases/2.7/
 

## Usage

***Initializing Script***

	python pacman.py
	python gridworld.py -m
	
***Value Iteration***

	python gridworld.py -a value -i 5
	
***Discounted Rewards***

	python gridworld.py -a value -i 100 -g DiscountGrid --discount 0.9 --noise 0.2 --livingReward 0.0
	
***Q-Learning***

	python pacman.py -p PacmanQAgent -x 2000 -n 2010 -l smallGrid 
	

## Unit Testing and Benchmarking

***Full Test***

	python autograder.py
	
***Single Test***

	python autograder.py -q q2
