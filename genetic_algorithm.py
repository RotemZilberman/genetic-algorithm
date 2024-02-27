from abc import ABC, abstractmethod

class GeneticAlgorithm(ABC):
    def __init__(self, population, generations, mutation, crossover, selection, tournament, output):
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
    def __init__(self, population, generations, mutation, crossover, selection, tournament, fitness, output):
        super().__init__(population, generations, mutation, crossover, selection, tournament, fitness, output)

    def generate_population(self):
        pass
    # using population of (x,y) swap between 2 random points with changece probebility by there difference
    def mutate(self, individual):
        pass

    # calculate the distance between the cities
    def fitness_function(self, individual):
        pass

    # first have and then go by the sec parent
    def crossover(self, parent1, parent2):
        pass

    def chromosome_to_solution(self, chromosome):
        return chromosome
