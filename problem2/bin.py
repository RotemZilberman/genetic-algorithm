import argparse
import math
from itertools import permutations
import time

from ..general.analyze_data import result_to_plot
from ..general.genetic_algorithm import TSP
from .city import City

Population = 100
Generations = 100
Patience = 10
MutationRate = 0.1
CrossoverRate = 0.9
EliteSize = 2


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", required=True, type=str)
    parser.add_argument("--exp-name", required=True, type=str)
    parser.add_argument("--methode", required=False, type=int, default=Population)
    args = parser.parse_args()
    return args


def extract_city_data(file):
    cities = {}
    with open(file, 'r') as f:
        lines = f.readlines()
        for index, line in enumerate(lines):
            x, y = line.split(' ')
            cities[index] = City(int(x), int(y))
    return cities


def compute_distance(start_city, path, cities):
    distance = 0
    current_city = start_city
    for city_index in path:
        city = cities[city_index]
        distance += current_city.distance(city)
        current_city = city
    distance += current_city.distance(start_city)
    return distance


def bf_solution(cities):
    min_distance = math.inf
    min_path = None
    start_city = cities[1]
    del cities[1]

    for path in permutations(list(cities), len(list(cities))):
        distance = compute_distance(start_city, path, cities)

        if distance < min_distance:
            min_distance = distance
            min_path = path

    return min_path, min_distance


def main():
    # collect data and arguments
    population, generations, patience, mutation_rate, crossover_rate, elite_size = (
        Population, Generations, Patience, MutationRate, CrossoverRate, EliteSize)
    args = get_args()
    cities = extract_city_data(args.data_dir)
    start_time = time.time()

    if args.method == "GA":
        gen_alg = TSP(population, generations, patience, mutation_rate, crossover_rate, elite_size, cities)
        best_eval_list, avg_eval_list, best_result = gen_alg.run()

        result_to_plot(best_eval_list, avg_eval_list, args.data_dir, args.exp_name)
        with open(f'{args.data_dir}/{args.exp_name}_best_result.txt', 'w') as f:
            for city_index in best_result:
                f.write(f'{city_index}\n')
        print(f'Best result: {best_result} with distance of {compute_distance(cities[1], best_result, cities)}')
    else:
        min_path, min_distance = bf_solution(cities)
        print(f'Best result: {min_path} with distance of {min_distance}')

    print(f'Execution time: {time.time() - start_time}')


if __name__ == '__main__':
    main()
