from random import getrandbits, choice, shuffle, random;  # used in merge_dna() to choose parent base
from math import sqrt;

class Being:
    @staticmethod
    def merge_dna(dna_parent_1, dna_parent_2):
        dna_array = [None]*16
        # for each dna base, randomly pick one base from parents
        for index in range(16):
            if (bool(getrandbits(1))):
                dna_array[index] = dna_parent_1[index];
            else:
                dna_array[index] = dna_parent_2[index];
        return dna_array;

    @staticmethod
    def random_dna():
        dna_bases = ['A', 'C', 'G', 'T']
        dna_array = [None]*16
        # for each dna base, randomly pick one base
        for index in range(16):
            dna_array[index] = choice(dna_bases);
        return dna_array;
    
    def get_survival_probability(self, optimal_base):
        saturation_level = self.dna.count(optimal_base) / len(self.dna);
        #return sqrt(saturation_level);
        return saturation_level;
    
    def __str__(self):
        string = "[";
        for (index, base) in enumerate(self.dna):
            string += base;
        string += "] Gen:{}".format(self.generation);
        return string;
    
    def __init__(self, this_generation:int, parent1=None, parent2=None):
        self.generation = this_generation;
        self.parent1 = parent1;
        self.parent2 = parent2;
        if ((parent1 == None) and (parent2 == None)):
            self.dna = self.random_dna();
        else:
            self.dna = self.merge_dna(parent1.dna, parent2.dna);

class Population:

    def replace_parent_with_child(self, parent, child):
        parent_index = self.population.index(parent);
        self.population[parent_index] = child;

    def mate(self, parent1, parent2):
        child1  = Being(self.generation, parent1, parent2);
        child2  = Being(self.generation, parent1, parent2);
        self.replace_parent_with_child(parent1, child1);
        self.replace_parent_with_child(parent2, child2);
    
    def mating_season(self):        
        # shuffle population to generate random consecutive pairs
        # match each consecutive being to procreate
        shuffle(self.population);
        # population must be even
        for index in range(0, len(self.population), 2):
            parent1 = self.population[index];
            parent2 = self.population[index+1];
            self.mate(parent1, parent2);
    
    def natural_selection(self):

        for index, being in enumerate(self.population):
            survival_prob = being.get_survival_probability(self.optimal_base);
            if (random() >= survival_prob):
                #being dies
                being_index = self.population.index(being);
                self.population[being_index] = None;
        
        # filter dead beings from population, ensure population size is even
        self.population = [being for being in self.population if being]
        if (len(self.population) % 2 != 0):
            del self.population[-1];

    def get_next_gen(self):
        self.generation += 1;
        self.natural_selection();
        self.mating_season();
    
    def advance_gen(self, count):
        for i in range(count):
            self.get_next_gen();

    def print_generation(self):
        print(" == Generation {} == ".format(self.generation));
        print(str(self));
        print(" =================== " + "\n");

    def __str__(self):
        pop_string = "";
        for index, being in enumerate(self.population):
            if (index != 0): 
                pop_string += "\n"
            pop_string += str(being);
        return pop_string;

    def __init__(self, size, optimal_base):
        if (size % 2 != 0):
            size += 1;
        self.generation = 0;
        self.population = [None] * size;
        self.optimal_base = optimal_base;
        for (index, base) in enumerate(self.population):
            self.population[index] = Being(self.generation);

pop = Population(10000, 'A');
pop.print_generation();

pop.advance_gen(7);
pop.print_generation();

    


# this_generation = 0;

# parent1 = Being(this_generation);
# parent2 = Being(this_generation);
# child1  = Being(this_generation, parent1, parent2);
# child2  = Being(this_generation, parent1, parent2);
# print("parent 1: \t"+ str(parent1));
# print("parent 2: \t"+ str(parent2));
# print("child 1: \t"+  str(child1));
# print("child 2: \t"+  str(child2));
