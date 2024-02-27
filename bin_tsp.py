import argparse

Population = 100
Generations = 100
Patience = 10
MutationRate = 0.1
CrossoverRate = 0.9
EliteSize = 2


def main():
    population, generations, patience, mutation_rate, crossover_rate, elite_size = (
        Population, Generations, Patience, MutationRate, CrossoverRate, EliteSize)
    gen_alg = TSP(population, generations, patience, mutation_rate, crossover_rate, elite_size)
    best_list, avg_eval_list, best_eval = gen_alg.run()


if __name__ == '__main__':
    main()
