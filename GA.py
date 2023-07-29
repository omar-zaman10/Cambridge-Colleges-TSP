import pandas as pd
import numpy as np
from pprint import pprint
import random
from config import colleges

class GA_Solver():


    '''
    Documentation given by ChatGPT

    The GA_Solver class is a Genetic Algorithm (GA) solver designed to find an optimal solution to the traveling salesman problem (TSP) using a genetic algorithm approach. The TSP involves finding the shortest possible route that visits a given set of cities and returns to the starting city, with each city visited only once. The solver tries to find the best permutation of colleges (cities) in Cambridge, based on a given distance matrix.

    Class Attributes:
    distance_matrix: A 2D matrix representing the distances between different colleges (cities) in Cambridge.

    population: A list of permutations representing the population of solutions. Each permutation is a possible order of colleges to visit.

    offspring: A list to store the newly generated offspring solutions during the recombination phase.

    population_size: An integer specifying the size of the population (number of permutations) to be generated.

    offspring_size: An integer specifying the number of offspring to be generated during the recombination phase.

    best_solution: A list representing the best solution found so far (shortest distance permutation).

    best_distance: A floating-point number representing the distance of the best solution found so far.

    generation: An integer indicating the current generation of the genetic algorithm.

    generation_limit: An integer specifying the maximum number of generations the GA will run.

    mutation_rate: A float representing the probability of mutation occurring in a solution during the mutation phase.

    colleges: A list of strings containing the names of colleges in Cambridge. This list represents the cities to be visited.

    mating_chances: A list of integers representing the mating chances of each permutation in the population. The chances are used in the recombination phase to select parents based on their fitness.

    Class Methods:
    __init__(self, distance_matrix): The constructor method initializes the GA_Solver object with a given distance matrix.

    reinitialize(self): This method reinitializes the solver's state by creating a new instance of the GA_Solver class with the same distance matrix.

    generate_population(self): Generates a new random population of permutations based on the given population_size.

    objective_function(self, permutation): Calculates the objective (fitness) value for a given permutation (route). The objective value represents the total distance traveled for the given route.

    update_mutation_rate(self): Updates the mutation rate by decreasing it using a decay factor.

    mutations(self): Applies mutations to the current population with a probability determined by the mutation_rate.

    mutate(self, perm): Performs mutation on a single permutation by swapping two elements randomly.

    recombination(self): Creates a new offspring population by performing recombination (breeding) on the current population.

    breed(self, p1, p2): Performs recombination (crossover) between two parent permutations to generate a child permutation.

    selection(self): Selects the best solutions (permutations) from both the current population and offspring to form the next population.

    solve(self): The main method that solves the TSP using the genetic algorithm. It runs the genetic algorithm for a specified number of generations.

    plot(self): A placeholder method to visualize the results (e.g., plot the best solution).

    Usage:
    Create an instance of the GA_Solver class, passing the distance matrix as an argument.

    Call the solve() method to find the best solution.

    Access the best_solution and best_distance attributes to retrieve the optimal solution and its distance, respectively.
    '''

    def __init__(self,distance_matrix) :
        self.distance_matrix = distance_matrix

        # Family of solutions and distances
        self.population = [] # List of permutations
        self.offspring = []

        self.population_size = 3000
        self.offspring_size = 5_000

        self.best_solution = None
        self.best_distance = float('infinity')

        self.generation = 0
        self.generation_limit = 100

        self.mutation_rate = 1


        self.colleges  = colleges

        #self.mapping = {i:self.colleges[i] for i in range(len(colleges))}
        self.mating_chances = [2*(self.population_size+1 -2*R) + 2*(R-1) for R in range(1,self.population_size+1)]


    def reinititalise(self):
        self.__init__(self.distance_matrix)


    def generate_population(self):
        self.population = []

        for _ in range(self.population_size):
            self.population.append(list(np.random.permutation(self.colleges)))

        self.population.sort(key= lambda x: self.objective_function(x))


    def objective_function(self,permutation):

        if len(permutation) != len(self.colleges):
            raise ValueError('Solution of permutation does not have all colleges')

        distance = 0

        for i in range(len(self.colleges)-1):

            distance += self.distance_matrix[permutation[i]][permutation[i+1]]
        
        distance += self.distance_matrix[permutation[-1]][permutation[0]]

        return distance

    def update_mutation_rate(self):

        alpha= 0.98
        self.mutation_rate *= alpha

    def mutations(self):
        for i,perm in enumerate(self.population):


            if random.random() < self.mutation_rate:
                
                q = self.mutate(perm)
                self.population[i] = q

        self.update_mutation_rate()
    
    def mutate(self,perm):
        i = random.randint(0,len(perm)-1)
        j = random.randint(0,len(perm)-1)


        perm[i],perm[j] = perm[j],perm[i]
        return perm



    def recombination(self):
        #discrete - choose two random permutations and recombine into an offspring
        self.offspring = []
        for i in range(self.offspring_size):
            p1,p2 = random.choices(self.population,k=2,weights=self.mating_chances)


            child = self.breed(p1,p2)
            self.offspring.append(child)


    def breed(self,p1,p2):
        child = None
        c1 = []
        c2 = []
        c3 = []

        a = random.randint(0,len(self.colleges))
        b = random.randint(0,len(self.colleges))

        start = min(a,b)
        end = max(a,b)


        for i in range(start,end):
            c1.append(p1[i])
        

        c2 = [d for d in p2 if d not in c1]
        
        c3 = c2[start:]
        c2 = c2[:start]

        child = c2 + c1 + c3
        return child
    

    def selection(self):
        elitist =  self.offspring + self.population 
        elitist.sort(key= lambda x : self.objective_function((x)))

        self.population = elitist[:self.population_size]

        d = self.objective_function(self.population[0])
        print(d)

        if self.best_distance > d:
            self.best_distance = d
            self.best_solution = self.population[0][:]


    def solve(self):
        self.generate_population()

        for i in range(self.generation_limit):
            
            self.recombination()
            self.selection()
            self.mutations()
            

    def plot(self):
        pass





if __name__ == '__main__':

    data = pd.read_csv('Data/Distances_table.csv')


    distance_dictionary = {college:{} for college in colleges}

    for college in colleges:
        for i,value in enumerate(data[college]):

            distance_dictionary[college][colleges[i]] = value




    solver = GA_Solver(distance_dictionary)

    best = ['Queens College Cambridge', 'Darwin College Cambridge', 'Newnham College Cambridge', 'Wolfson College Cambridge',
             'Selwyn College Cambridge', 'Clare Hall Cambridge', 'Robinson College Cambridge', 'St Johns College Cambridge',
               'Lucy Cavendish College Cambridge', 'St Edmunds College Cambridge', 'Murray Edwards College Cambridge',
                 'Girton College Cambridge', 'Fitzwilliam College Cambridge', 'Churchill College Cambridge',
                   'Magdalene College Cambridge', 'Trinity College Great Court Cambridge', 'Trinity Hall Cambridge',
                     'Clare College Cambridge', 'Kings College Cambridge', 'Gonville and Caius College Cambridge',
                       'Jesus College Cambridge', 'Sidney Sussex College Cambridge', 'Christs College Cambridge',
                         'Emmanuel College Cambridge', 'Hughes Hall Cambridge', 'Homerton College Cambridge',
                           'Downing College Cambridge', 'Peterhouse Cambridge', 'Pembroke College Cambridge', 
                           'Corpus Christi College Cambridge', 'St Catharines College Cambridge']
    
    
    print(solver.objective_function(best))


    print('-'*160)

    solver.solve()



    print('-'*160)
    print('-'*160)

    print(solver.best_solution)

    print(solver.best_distance)

