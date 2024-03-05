import random
import math
from abc import ABC, abstractmethod


def calculate_x(m):
    # Calculate the discriminant
    discriminant = 1 + 8 * m

    # Check if the discriminant is non-negative
    if discriminant >= 0:
        # Calculate the positive value of x
        x = (-1 + discriminant ** 0.5) / 2
        return math.floor(x)
    else:
        return 0


class GeneticAlgorithm(ABC):
    def __init__(self, population, generations, patience, mutation_rate, crossover_rate, elite_size):
        self.population = population
        self.generations = generations
        self.patience = patience
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.elite_size = elite_size

    @abstractmethod
    def generate_population(self):
        pass

    @abstractmethod
    def mutate(self, individual):
        pass

    def get_elite(self, pop_eval):
        top = pop_eval[-1 * self.elite_size:]
        return [chromo for (chromo, evaluation) in top]

    @abstractmethod
    def fitness_function(self, individual):
        pass

    def evaluate_all(self, population):
        pop_eval = []
        for chromo in population:
            pop_eval.append((chromo, self.fitness_function(chromo)))

        def key(element):
            return element[1]

        pop_eval.sort(key=key)
        best_eval = pop_eval[-1][1]
        avg_eval = 0
        for element in pop_eval:
            avg_eval += element[1]
        avg_eval /= self.population
        return pop_eval, avg_eval, best_eval

    def sample_chromos(self, pop_eval):
        combinations = (self.population * (self.population - 1)) / 2
        rand1 = random.randint(0, combinations)
        rand2 = random.randint(0, combinations)
        first = pop_eval[calculate_x(rand1)][0]
        second = pop_eval[calculate_x(rand2)][0]
        return first, second

    @abstractmethod
    def crossover(self, parent1, parent2):
        pass

    def evolve(self, pop_eval):
        population = self.get_elite(pop_eval)
        count = 0
        while count < (self.population - self.elite_size):
            first, second = self.sample_chromos(pop_eval)
            child1, child2 = self.crossover(first, second)
            population.append(child1)
            population.append(child2)
            count += 2

        return population

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

        pop_eval, avg_eval, best_eval = self.evaluate_all(population)
        return best_list, avg_eval_list, pop_eval[-1][0]


class TSP(GeneticAlgorithm):
    def __init__(self, population, generations, patience, mutation_rate, crossover_rate, elite_size, cities,
                 cross_mode="single"):
        super().__init__(population, generations, patience, mutation_rate, crossover_rate, elite_size)
        if cross_mode == "Cycle Crossover":
            self.cities = cities
            self.cross_mode = cross_mode
        else:
            self.start_city = cities[1]
            self.cities = cities
            del cities[1]
            self.cross_mode = cross_mode

    def generate_population(self):
        pop_size = self.population
        population = []
        for _ in range(pop_size):
            population.append(random.sample(list(self.cities), len(self.cities)))
        return population

    def mutate(self, individual):
        if random.random() < self.mutation_rate:
            index1, index2 = random.sample(range(len(individual)), 2)
            individual[index1], individual[index2] = individual[index2], individual[index1]

    def fitness_function(self, individual):
        current_distance = 0
        if self.cross_mode == "Cycle Crossover":
            current_city = self.cities[individual[0]]
            for city_index in individual:
                city = self.cities[city_index]
                current_distance += current_city.distance(city)
                current_city = city
            current_distance += current_city.distance(self.cities[individual[0]])
        else:
            current_city = self.start_city
            for city_index in individual:
                city = self.cities[city_index]
                current_distance += current_city.distance(city)
                current_city = city
            current_distance += current_city.distance(self.start_city)
        return 1 / current_distance

    def crossover(self, parent1, parent2):

        def combine(p1, p2, single_point):
            child = p1[:single_point]
            for city in p2:
                if city not in child:
                    child.append(city)
            return child

        def Cycle_Crossover_combine(p1, p2):      # Cycle Crossover crossover
            p1_copy = list(p1)
            p2_copy = list(p2)
            p1 = list(p1)
            p2 = list(p2)
            childx, childy = [], []
            starting_city = random.choice(p1)
            c1 = p1.index(starting_city)
            c2 = p2.index(starting_city)
            while True:
                val = p1[c1]
                next_city_x = p1[(c1 + 1) % len(p1)]
                next_city_y = p2[(c2 + 1) % len(p2)]
                dx = self.cities[p1[c1]].distance(self.cities[next_city_x])
                dy = self.cities[p2[c2]].distance(self.cities[next_city_y])
                childx.append(val)
                p1.remove(val)
                p2.remove(val)
                if dx <= dy:
                    c1 = p1.index(next_city_x)
                    c2 = p2.index(next_city_x)
                else:
                    c1 = p1.index(next_city_y)
                    c2 = p2.index(next_city_y)
                if len(p1) == 1:
                    childx.append(p1[0])
                    break
            p1 = p1_copy
            p2 = p2_copy
            c1 = p1.index(starting_city)
            c2 = p2.index(starting_city)
            while True:
                val = p1[c1]
                prev_city_x = p1[(c1 - 1) % len(p1)]
                prev_city_y = p2[(c2 - 1) % len(p2)]
                dx = self.cities[p1[c1]].distance(self.cities[prev_city_x])
                dy = self.cities[p2[c2]].distance(self.cities[prev_city_y])
                childy.append(val)
                p1.remove(val)
                p2.remove(val)
                if dx <= dy:
                    c1 = p1.index(prev_city_x)
                    c2 = p2.index(prev_city_x)
                else:
                    c1 = p1.index(prev_city_y)
                    c2 = p2.index(prev_city_y)
                if len(p1) == 1:
                    childy.append(p1[0])
                    break
            return childx, childy

        child1 = []
        child2 = []
        seed = random.uniform(0, 1)
        if seed <= self.crossover_rate:
            if self.cross_mode == "single":
                point = random.randint(0, len(parent1) - 1)
                child1 = combine(parent1, parent2, point)
                child2 = combine(parent2, parent1, point)
            elif self.cross_mode == "double-point":
                point1 = random.randint(0, len(parent1) - 1)
                point2 = random.randint(0, len(parent1) - 1)
                child1 = combine(parent1, parent2, point1)
                child2 = combine(parent2, parent1, point2)
            elif self.cross_mode == "Cycle Crossover":
                child1, child2 = Cycle_Crossover_combine(parent1.copy(), parent2.copy())
        else:
            child1 = parent1.copy()
            child2 = parent2.copy()
        self.mutate(child1)
        self.mutate(child2)
        return child1, child2
