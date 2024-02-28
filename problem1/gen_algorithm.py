import random
from abc import ABC, abstractmethod


class GeneticAlgorithm(ABC):
    def __init__(self, population, generations, patience, mutation_rate, crossover_rate, elite_size):
        pass

    @abstractmethod
    def generate_population(self):
        pass

    @abstractmethod
    def mutate(self, individual):
        pass

    def getElite(self, pop_eval):
        pass

    @abstractmethod
    def fitness_function(self, individual):
        pass

    def evaluate_all(self, population):
        pass

    def evolve(self, pop_eval):
        pass

    @abstractmethod
    def crossover(self, parent1, parent2):
        pass

    def chromosome_to_solution(self, chromosome):
        return chromosome

    def run(self):
        # Create initial population
        population = self.generate_population()
        best_list = []
        avg_eval_list = []
        # Run through generations
        for i in range(self.generations):
            print(f'Generation {i + 1}...')

            pop_eval, avg_eval, best_eval = self.evaluate_all(population)
            best_list.append(best_eval)
            avg_eval_list.append(avg_eval)

            population = self.evolve(pop_eval)

        return best_list, avg_eval_list, best_list[-1]


class EightQueenPuzzle(GeneticAlgorithm):
    def __init__(self, population, generations, mutation, crossover, selection, tournament, fitness, output):
        super().__init__(population, generations, mutation, crossover, selection, tournament, fitness, output)

    def generate_population(self):
        pass

    # easy to implement - just generate gosian noise between 1-8 for each queen
    def mutate(self, individual):
        pass

    # count the conflicts between the queens
    def fitness_function(self, individual):
        pass

    # checking between multiple single points and uniform crossover
    def crossover(self, parent1, parent2):
        pass


class TSP(GeneticAlgorithm):
    def __init__(self, population, generations, patience, mutation_rate, crossover_rate, elite_size, cities):
        super().__init__(population, generations, patience, mutation_rate, crossover_rate, elite_size)
        self.start_city = cities[1]
        self.cities = cities
        del cities[1]

    def generate_population(self):
        pop_size = self.population
        population = []
        for _ in range(pop_size):
            population.append(random.sample(self.cities.keys(), len(self.cities)))
        return population

    def mutate(self, individual):
        if random.random() < self.mutation_rate:
            index1, index2 = random.sample(range(len(individual)), 2)
            individual[index1], individual[index2] = individual[index2], individual[index1]

    def fitness_function(self, individual):
        current_distance = 0
        current_city = self.start_city
        for city_index in individual:
            city = self.cities[city_index]
            current_distance += current_city.distance(city)
            current_city = city
        current_distance += current_city.distance(self.start_city)
        return 1 / current_distance

    def crossover(self, parent1, parent2):
        single_point = self.population // 2
        child = parent1[:single_point]
        for city in parent2:
            if city not in child:
                child.append(city)
        return child

    def chromosome_to_solution(self, chromosome):
        return chromosome
