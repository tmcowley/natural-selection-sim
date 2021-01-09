from random import  getrandbits;
from random import  choice;
from random import  shuffle;
from random import  random;
from random import  sample;
from random import  randint;

from math import    sqrt;
from math import    floor;

class Being:
    dna_bases   = ['A', 'C', 'G', 'T'];
    survival_prob_exponent = 3.5;

    def is_child_of(self, being):
        is_parent = (self.parent1 == being or self.parent2 == being);
        return (is_parent);

    @staticmethod
    def genetic_mutation():
        # 1 in 1000 chance
        return (randint(1, 1000) == 1);

    @staticmethod
    def merge_dna(dna_parent_1, dna_parent_2):
        dna_array = [None]*16;
        # for each dna base, randomly pick one base from parents
        for index in range(16):
            if (Being.genetic_mutation()):
                dna_array[index] = choice(Being.dna_bases);
            elif (bool(getrandbits(1))):
                dna_array[index] = dna_parent_1[index];
            else:
                dna_array[index] = dna_parent_2[index];
        return dna_array;

    @staticmethod
    def random_dna():
        dna_array = [None]*16;
        # for each dna base, randomly pick one base
        for index in range(16):
            dna_array[index] = choice(Being.dna_bases);
        return dna_array;
    
    def get_survival_probability(self, optimal_base, current_generation):
        if (current_generation - self.generation >= 4):
            return 0; # senicide
        dna_optimal_base_proportion = self.dna.count(optimal_base) / len(self.dna);
        #print("given a {}% chance to live".format((dna_optimal_base_proportion**2)*100));
        return (dna_optimal_base_proportion**Being.survival_prob_exponent);
    
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
        if ((parent1 == None) or (parent2 == None)):
            self.dna = Being.random_dna();
        else:
            self.dna = Being.merge_dna(parent1.dna, parent2.dna);

class Population:
    max_pop             = 50000;
    critical_high_pop   = 10000;
    critical_low_pop    = 500;
    reproduction_factor = 4;

    @staticmethod
    def are_related(being1, being2):
        # check if being2 is a parent of being1, and if being1 is a parent of being2
        related = (being1.is_child_of(being2) or being2.is_child_of(being1));
        return related;
    
    @staticmethod
    def being_is_optimal(being, optimal_base):
        for base in being.dna:
            if (base != optimal_base):
                return False;
        return True;

    def replace_parent_with_child(self, parent, child):
        parent_index = self.population.index(parent);
        self.population[parent_index] = child;

    @staticmethod
    def mate(generation, parent1, parent2): 
        return Being(generation, parent1, parent2);
    
    def mating_season(self): 
        # shuffle population to improve randomness
        shuffle(self.population);

        # empty list, storing offspring
        # let n be the current population size, allow kn reproductions
        offspring = [None]*floor(self.reproduction_factor*(len(self.population)));

        for index in range(len(offspring)):
            mating_pair = sample(self.population, 2);
            candidate1 = mating_pair[0];
            candidate2 = mating_pair[1];
            if (Population.are_related(candidate1, candidate2)):
                continue;
            offspring[index] = Population.mate(self.generation, candidate1, candidate2);
        
        # merge offspring array with general population
        offspring = [child for child in offspring if child];
        self.population += offspring;
    
    def test_fitness(self): 
        # empty list, storing survivors 
        survivors = [None]*len(self.population);

        # test fitness of each member of the population
        for index, being in enumerate(self.population):
            survival_prob = being.get_survival_probability(self.optimal_base, self.generation);
            if (random() < survival_prob):
                #being lives
                survivors[index] = being;

        # filter dead beings from survivors, set to population
        self.population = [being for being in survivors if being]
        print ("survived: {}".format(len(self.population)));

    def control_population(self):
        if (len(self.population) <= Population.critical_low_pop):
            # increase reproduction rate, halve exp
            self.reproduction_factor += 1;
            Being.survival_prob_exponent *= 0.5;
        if (len(self.population) >= Population.critical_high_pop):
            # halve reproduction rate, double exp
            self.reproduction_factor *= 0.5;
            Being.survival_prob_exponent *= 2;

    def get_next_gen(self):
        self.generation += 1;
        self.control_population();
        self.test_fitness();
        if (len(self.population) > 1):
            self.mating_season();
    
    def advance_gen(self, count):
        for i in range(count):
            self.get_next_gen();
            print("Gen {} completed, pop:{}".format(self.generation, len(self.population)));
            if (len(self.population) < 1):
                break;
    
    def get_rand_being_in_population(self):
        return choice(self.population);

    def print_generation(self):
        if (len(self.population) == 0):
            return "\n";
        gen_desc    = " ==== Generation {} ==== \n".format(self.generation);
        gen_end     = "\n {} \n".format("="*(len(gen_desc)-3));
        print(gen_desc + str(self) + gen_end);

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

optimal_base = choice(Being.dna_bases);

pop = Population(5000, optimal_base);
pop.print_generation();

pop.advance_gen(30);
pop.print_generation();

random_being = pop.get_rand_being_in_population();

if (Population.being_is_optimal(random_being, optimal_base)):
    print("Population is likely optimal.\n");
else:
    print("Population is unlikely optimal.\n");