# Genetic Algorithm for 8-Queens and Traveling Salesman Problem
This repository hosts implementations of two classic problems in computer science: the 8-Queens problem and the Traveling Salesman Problem (TSP) solved using Genetic Algorithm (GA).

## Introduction
Genetic Algorithm is a heuristic search algorithm inspired by the principles of natural selection and genetics. It's commonly used to find approximate solutions to optimization and search problems. This algorithm works by evolving a population of candidate solutions over successive generations through processes such as selection, crossover, and mutation, mimicking the process of natural selection.

## 8-Queens Problem
In the 8-Queens problem, the objective is to place eight chess queens on an 8×8 chessboard so that no two queens threaten each other. Thus, a solution requires that no two queens share the same row, column, or diagonal.

## Traveling Salesman Problem (TSP)
The Traveling Salesman Problem involves finding the shortest possible route that visits each city exactly once and returns to the origin city. It is a classic optimization problem in the field of combinatorial optimization and is known to be NP-hard.

## How Genetic Algorithm Works
- Initialization: Randomly generate an initial population of candidate solutions.
- Evaluation: Calculate the fitness of each candidate solution in the population.
- Selection: Select the best-fit individuals (parents) from the population for reproduction.
- Crossover: Create new candidate solutions by combining genetic material (chromosomes) of the selected parents.
- Mutation: Introduce random changes in the offspring to maintain genetic diversity.
- Replacement: Replace the least fit individuals in the population with the new offspring.
- Termination: Repeat steps 2-6 until a termination condition is met (e.g., a maximum number of generations is reached, or an acceptable solution is found).
  
## Repository Structure
- problem1: Python implementation of the Genetic Algorithm for solving the 8-Queens problem.
- problem2: Python implementation of the Genetic Algorithm for solving the Traveling Salesman Problem.
- README.md: This file containing information about the repository and its contents.
  
## Contributions
Contributions to improve the implementations or add new features are welcome. Feel free to open a pull request or create an issue to discuss potential enhancements or fixes.

### License
This project is licensed under the MIT License - see the LICENSE file for details.
