import random

import numpy as np
import pandas as pd

from config import colleges

class GeneticAlgorithmSolver:
    """
    Class Methods:
    __init__(self, distance_matrix): The constructor method initializes the GeneticAlgorithmSolver object with a given distance matrix.

    _generate_population(self): Generates a new random population of permutations based on the given population_size.

    objective_function(self, permutation): Calculates the objective (fitness) value for a given permutation (route). The objective value represents the total distance traveled for the given route.

    _update_mutation_rate(self): Updates the mutation rate by decreasing it using a decay factor.

    _mutations(self): Applies mutations to the current population with a probability determined by the mutation_rate.

    _mutate(self, perm): Performs mutation on a single permutation by swapping two elements randomly.

    _recombination(self): Creates a new offspring population by performing recombination (breeding) on the current population.

    _breed(self, parent1, parent2): Performs _recombination (crossover) between two parent permutations to generate a child permutation.

    _selection(self): Selects the best solutions (permutations) from both the current population and offspring to form the next population.

    solve(self): The main method that solves the TSP using the genetic algorithm. It runs the genetic algorithm for a specified number of generations.

    Usage:
    Create an instance of the GA_Solver class, passing the distance matrix as an argument.

    Call the solve() method to find the best solution.

    Access the best_solution and best_distance attributes to retrieve the optimal solution and its distance, respectively.
    """

    def __init__(self, distance_matrix):
        self.distance_matrix = distance_matrix

        self._population = []
        self._offspring = []

        self._population_size = 3000
        self._offspring_size = 5_000

        self._best_solution = None
        self._best_distance = float("infinity")

        self._generation = 0
        self._generation_limit = 100

        self._mutation_rate = 1

        self._colleges = colleges

        self._mating_chances = [
            2 * (self._population_size + 1 - 2 * R) + 2 * (R - 1)
            for R in range(1, self._population_size + 1)
        ]

    def _generate_population(self):
        self._population = []

        for _ in range(self._population_size):
            self._population.append(list(np.random.permutation(self._colleges)))

        self._population.sort(key=lambda x: self.objective_function(x))

    def objective_function(self, permutation):
        if len(permutation) != len(self._colleges):
            raise ValueError("Solution of permutation does not have all colleges")

        distance = 0

        for i in range(len(self._colleges) - 1):
            distance += self.distance_matrix[permutation[i]][permutation[i + 1]]

        distance += self.distance_matrix[permutation[-1]][permutation[0]]

        return distance

    def _update_mutation_rate(self):
        alpha = 0.98
        self._mutation_rate *= alpha

    def _mutations(self):
        for i, perm in enumerate(self._population):
            if random.random() < self._mutation_rate:
                q = self._mutate(perm)
                self._population[i] = q

        self._update_mutation_rate()

    def _mutate(self, perm):
        i = random.randint(0, len(perm) - 1)
        j = random.randint(0, len(perm) - 1)

        perm[i], perm[j] = perm[j], perm[i]
        return perm

    def _recombination(self):
        # discrete - choose two random permutations and recombine into an offspring
        self._offspring = []
        for i in range(self._offspring_size):
            p1, p2 = random.choices(self._population, k=2, weights=self._mating_chances)

            child = self._breed(p1, p2)
            self._offspring.append(child)

    def _breed(self, parent1, parent2):
        section1 = []

        a = random.randint(0, len(self._colleges))
        b = random.randint(0, len(self._colleges))

        start = min(a, b)
        end = max(a, b)

        for i in range(start, end):
            section1.append(parent1[i])

        section2 = [d for d in parent2 if d not in section1]

        section3 = section2[start:]
        section2 = section2[:start]

        child = section2 + section1 + section3
        return child

    def _selection(self):
        elitist = self._offspring + self._population
        elitist.sort(key=lambda x: self.objective_function((x)))

        self._population = elitist[: self._population_size]

        current_distance = self.objective_function(self._population[0])

        if self._best_distance > current_distance:
            print(f"Updating best distance to {current_distance}")
            self._best_distance = current_distance
            self._best_solution = self._population[0][:]

    def solve(self):
        self._generate_population()

        for _ in range(self._generation_limit):
            self._recombination()
            self._selection()
            self._mutations()

        return [str(x) for x in self._best_solution]



if __name__ == "__main__":
    data = pd.read_csv("Data/Distances_table.csv")

    distance_dictionary = {college: {} for college in colleges}

    for college in colleges:
        for i, value in enumerate(data[college]):
            distance_dictionary[college][colleges[i]] = value

    solver = GeneticAlgorithmSolver(distance_dictionary)

    print("-" * 50)

    best_solution = solver.solve()

    print("-" * 50)
    print("-" * 50)

    print("Shortest path found")
    print(best_solution)

    print(f"Shortest distance found {solver._best_distance}")
