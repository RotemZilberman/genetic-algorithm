import argparse
from gen_algorithm import EightQueenPuzzle

Population = 100
Generations = 1000
Patience = 10
MutationRate = 0.1
CrossoverRate = 0.1
EliteSize = 2


def main():
    population, generations, patience, mutation_rate, crossover_rate, elite_size = (
        Population, Generations, Patience, MutationRate, CrossoverRate, EliteSize)
    gen_alg = EightQueenPuzzle(population, generations, patience, mutation_rate, crossover_rate, elite_size)
    best_list, avg_eval_list, best_eval = gen_alg.run()
    print(f'{best_list[0]} to {best_list[-1]}')
    # print(gen_alg.fitness_function([0, 4, 7, 5, 2, 6, 1, 3]))


if __name__ == '__main__':
    main()
