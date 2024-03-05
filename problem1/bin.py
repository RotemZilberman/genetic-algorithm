import argparse
import time

from gen_algorithm import EightQueenPuzzle
from analyze_data import result_to_plot

BoardSize = 8
Population = 1000
Generations = 500
MutationRate = 0.01
CrossoverRate = 0.7
EliteSize = 18
CrossMode = "single"


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--method", required=False, type=str, default="GA")
    args = parser.parse_args()
    return args


def main():
    args = get_args()
    population, generations, mutation_rate, crossover_rate, elite_size, cross_mode = (
        Population, Generations, MutationRate, CrossoverRate, EliteSize, CrossMode)
    gen_alg = EightQueenPuzzle(population, generations, mutation_rate, crossover_rate, elite_size, cross_mode)
    if args.method == "GA":
        start = time.time()
        best_list, avg_eval_list, best_chromo = gen_alg.run()
        print("time: ", (time.time() - start))

    else:  # brute-force solution
        found = 0
        start = time.time()
        for i in range(8):
            for j in range(8):
                for k in range(8):
                    for l in range(8):
                        for m in range(8):
                            for n in range(8):
                                for o in range(8):
                                    for p in range(8):
                                        solution = [i, j, k, l, m, n, o, p]

                                        if gen_alg.fitness_function(solution) == BoardSize * (BoardSize - 1):
                                            print(solution, time.time() - start)
                                            found += 1

        if found == 0:
            print("Couldn't find a solution")


if __name__ == '__main__':
    main()
