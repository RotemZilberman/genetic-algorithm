import math
from abc import ABC, abstractmethod
import random


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

    # def sample_chromos(self, pop_eval):
    #     rand1 = random.randint(0, self.population-1)
    #     rand2 = random.randint(0, self.population-1)
    #     first = pop_eval[rand1][0]
    #     second = pop_eval[rand2][0]
    #     return first, second

    def sample_chromos(self, pop_eval):
        combinations = (self.population * (self.population-1))/2
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
            seed = random.uniform(0, 1)
            if seed <= self.crossover_rate:
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

        def key(element):
            return self.fitness_function(element)

        population.sort(key=key)
        return best_list, avg_eval_list, population[-1]


class EightQueenPuzzle(GeneticAlgorithm):
    def __init__(self, population, generations, patience, mutation_rate, crossover_rate, elite_size, cross_mode="single"):
        super().__init__(population, generations, patience, mutation_rate, crossover_rate, elite_size)
        self.cross_mode = cross_mode
        self.board_length = 8

    def generate_population(self):
        population = []
        for i in range(self.population):
            rand = random.choices(range(0, self.board_length), k=self.board_length)
            while not self.fitness_function(rand) < 20:
                rand = random.choices(range(0, self.board_length), k=self.board_length)
            population.append(rand)
        return population

    # easy to implement - just generate gosian noise between 1-8 for each queen
    def mutate(self, individual):
        seed = random_number = random.uniform(0, 1)
        if seed < self.mutation_rate:
            column = random.randint(0, self.board_length-1)
            index = random.randint(0, self.board_length-1)
            individual[column] = index
        return individual

    # checking between multiple single points and uniform crossover
    def crossover(self, parent1, parent2):
        child1 = []
        child2 = []
        if self.cross_mode == "single":
            point = random.randint(0, self.board_length-1)
            child1 = parent1[:point+1] + parent2[point+1:]
            child2 = parent2[:point+1] + parent1[point+1:]
        elif self.cross_mode == "uniform":
            for i in range(self.board_length):
                seed = random.uniform(0, 1)
                index1 = parent1[i] if seed <= 0.5 else parent2[i]
                index2 = parent2[i] if seed <= 0.5 else parent1[i]
                child1.append(index1)
                child2.append(index2)
        child1 = self.mutate(child1)
        child2 = self.mutate(child2)
        return child1, child2

    # count the conflicts between the queens
    def fitness_function(self, individual):
        hits = 0

        for col1, row1 in enumerate(individual):
            for col2, row2 in enumerate(individual):
                if col1 != col2:
                    hits += (row1 == row2)  # same row
                    hits += (((col2-col1) + row1) == row2) or ((row1 - (col2-col1)) == row2)  # same diagonal

        maximum_collisions = (self.board_length * (self.board_length-1))
        return maximum_collisions - hits

