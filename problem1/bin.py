import argparse
from gen_algorithm import EightQueenPuzzle
from analyze_data import result_to_plot

BoardSize = 8
Population = 100
Generations = 1000
Patience = 10
MutationRate = 0.1
CrossoverRate = 0.1
EliteSize = 2


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--method", required=False, type=str, default="bf")
    args = parser.parse_args()
    return args


def main():
    args = get_args()
    population, generations, patience, mutation_rate, crossover_rate, elite_size = (
        Population, Generations, Patience, MutationRate, CrossoverRate, EliteSize)
    gen_alg = EightQueenPuzzle(population, generations, patience, mutation_rate, crossover_rate, elite_size)
    if args.method == "GA":
        best_list, avg_eval_list, best_chromo = gen_alg.run()
        print(best_chromo)
        print(f'{best_list[0]} to {best_list[-1]}')
        if best_list[-1] == BoardSize * (BoardSize - 1):
            result_to_plot(best_list, avg_eval_list, "", "first")

    else:  # brute-force solution
        found = False
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
                                            print(solution)
                                            found = True
                                            return
        if not found:
            print("Couldn't find a solution")


if __name__ == '__main__':
    main()
