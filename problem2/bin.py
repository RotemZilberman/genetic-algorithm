import argparse
import math
import time
from itertools import permutations

from analyze_data import result_to_plot
from city import City
from gen_algorithm import TSP

Population = 200
Generations = 500
MutationRate = 0.01
CrossoverRate = 0.8
EliteSize = int(Population * 0.01)
cross_mode = "Cycle Crossover"


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
    if path[0] != 1:
        path = [1] + list(path)
    current_city = cities[path[0]]
    for city_index in path:
        city = cities[city_index]
        distance += current_city.distance(city)
        current_city = city
    distance += current_city.distance(cities[1])
    return distance


def brute_force_solution(cities):
    path = list(cities.keys())
    min_distance = math.inf
    min_path = None
    path = path[1:]
    for one_path in permutations(path):
        distance = compute_distance(one_path, cities)
        if distance < min_distance:
            min_distance = distance
            min_path = one_path
    return min_path, min_distance


def sort_order_by_leading_1(path):
    leading_1 = path.index(1)
    return path[leading_1:] + path[:leading_1]


def greedy_solution(cities):
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
        Population, Generations, 0, MutationRate, CrossoverRate, EliteSize)
    args = get_args()
    cities = extract_city_data(args.data_dir)
    start_time = time.time()
    if args.method == "ga":  # genetic algorithm
        gen_alg = TSP(population, generations, patience, mutation_rate, crossover_rate, elite_size, cities.copy()
                      , cross_mode)
        best_eval_list, avg_eval_list, best_result = gen_alg.run()
        if cross_mode != "Cycle Crossover":
            best_result = [1] + best_result
        else:
            best_result = sort_order_by_leading_1(best_result)
        result_to_plot(best_eval_list, avg_eval_list, args.data_dir, args.exp_name)
        with open(f'{args.data_dir}/{args.exp_name}_best_result.txt', 'w') as f:
            for city_index in best_result:
                f.write(f'\n{city_index}')
        print(f'Best result: {best_result} with distance of {compute_distance(best_result, cities)}')

    elif args.method == "bf":  # brute force
        min_path, min_distance = brute_force_solution(cities)
        print(f'Best result: {min_path} with distance of {compute_distance(min_path, cities)}')

    else:  # greedy solution
        min_path, min_distance = greedy_solution(cities)
        print(f'Best result: {min_path} with distance of {min_distance}')

    print(f'Execution time: {time.time() - start_time}')


if __name__ == '__main__':
    main()
