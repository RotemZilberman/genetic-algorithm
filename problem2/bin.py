import argparse
import math
import time

from analyze_data import result_to_plot
from city import City
from gen_algorithm import TSP

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
    parser.add_argument("--method", required=False, type=str, default="bf")
    args = parser.parse_args()
    return args


def extract_city_data(data_dir):
    file = f'{data_dir}/data.txt'
    cities = {}
    with open(file, 'r') as f:
        lines = f.readlines()
        for index, line in enumerate(lines):
            line = " ".join(line.split())
            x, y = line.split(" ")
            cities[index + 1] = City(int(x), int(y))
    return cities


def compute_distance(path, cities):
    distance = 0
    current_city = cities[path[0]]
    for city_index in path:
        city = cities[city_index]
        distance += current_city.distance(city)
        current_city = city
    distance += current_city.distance(cities[1])
    return distance


def greedy_solution(cities):
    start_city = cities[1]
    unvisited = list(cities.keys())
    unvisited.remove(1)
    path = [1]
    while unvisited:
        closest_dis = math.inf
        current_city = None
        for city_index in unvisited:
            dist = cities[path[-1]].distance(cities[city_index])
            if dist < closest_dis:
                current_city = city_index
                closest_dis = dist
        path.append(current_city)
        unvisited.remove(current_city)
    return path, compute_distance(path, cities)


def main():
    # collect data and arguments
    population, generations, patience, mutation_rate, crossover_rate, elite_size = (
        Population, Generations, Patience, MutationRate, CrossoverRate, EliteSize)
    args = get_args()
    cities = extract_city_data(args.data_dir)
    start_time = time.time()

    if args.method == "GA":  # genetic algorithm
        gen_alg = TSP(population, generations, patience, mutation_rate, crossover_rate, elite_size, cities)
        best_eval_list, avg_eval_list, best_result = gen_alg.run()

        result_to_plot(best_eval_list, avg_eval_list, args.data_dir, args.exp_name)
        with open(f'{args.data_dir}/{args.exp_name}_best_result.txt', 'w') as f:
            f.write(f'{1}')
            for city_index in best_result:
                f.write(f'\n{city_index}')
        print(f'Best result: {best_result} with distance of {compute_distance(cities[1], best_result, cities)}')

    else:  # greedy solution
        min_path, min_distance = greedy_solution(cities)
        print(f'Best result: {min_path} with distance of {min_distance}')

    print(f'Execution time: {time.time() - start_time}')


if __name__ == '__main__':
    main()
