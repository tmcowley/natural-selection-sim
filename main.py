from random import getrandbits  # to merge DNA
from random import choice       # to merge DNA
from random import shuffle      # to assist random mating
from random import random       # to generate random initial pop
from random import sample       # to choose mating partners
from random import randint      # to generate a random mutation

from typing import TypeVar  # duck typing
from typing import List     # duck typing
from math   import floor    # storing offspring, and pretty output
from time   import sleep    # stagger user output

# Duck typing: creating class: Being, Population types
BeingType   = TypeVar('BeingType',  bound='Being')
PopType     = TypeVar('PopType',    bound='Population')

class Being:
    dna_bases   = ['A', 'C', 'G', 'T']
    survival_prob_exponent = 3.5
    mutation_rate_denominator = 1000

    def is_child_of(self, being: BeingType) -> bool:
        ''' Assess if this being instance is the child of the given being '''
        return being in (self.parent1, self.parent2)

    @staticmethod
    def genetic_mutation() -> bool:
        ''' Simulate mutation: 1 in (mutation_rate_denom) chance of returning True '''
        return randint(1, Being.mutation_rate_denominator) == 1

    @staticmethod
    def merge_dna(dna_parent_1: List[str], dna_parent_2: List[str]) -> List[str]:
        ''' Randomly merge given DNA lists to create offspring DNA '''
        dna_array = [None]*16
        # for each dna base, randomly pick one base from parents
        for index in range(16):
            if Being.genetic_mutation():
                dna_array[index] = choice(Being.dna_bases)
            elif bool(getrandbits(1)):
                dna_array[index] = dna_parent_1[index]
            else:
                dna_array[index] = dna_parent_2[index]
        return dna_array

    @staticmethod
    def random_dna() -> List[str]:
        ''' Generate random DNA '''
        dna_array = [None]*16
        # for each dna base, randomly pick one base
        for index in range(16):
            dna_array[index] = choice(Being.dna_bases)
        return dna_array

    def get_survival_probability(self, optimal_base: str, current_generation: int) -> int:
        ''' Calculate a Being's survival probability, return is [0, 1] '''
        # Being is unfit if older than 4 generations
        if (current_generation - self.generation) >= 4:
            return 0
        # calculate similarity (0: nonoptimal, 1: perfectly optimal)
        dna_optimal_base_proportion = self.dna.count(optimal_base) / len(self.dna)
        # scale similarity with exponent > 1, this makes survival more selective
        return dna_optimal_base_proportion**Being.survival_prob_exponent

    def __len__(self) -> int:
        return len(str(self))

    def __str__(self) -> str:
        ''' String representation of a Being, of the form: [DNA] Gen: '''
        being_str = '[' + ''.join(self.dna) + "] Gen:{}".format(self.generation)
        return being_str

    def __init__(self, this_generation: int, parent1=None, parent2=None) -> BeingType:
        ''' Constructor -> generate being (from parents) '''
        self.generation = this_generation
        self.parent1 = parent1
        self.parent2 = parent2
        if None in (parent1, parent2):
            self.dna = Being.random_dna()
        else:
            self.dna = Being.merge_dna(parent1.dna, parent2.dna)

class Population:
    max_pop             = 50000
    critical_high_pop   = 10000
    critical_low_pop    = 500
    reproduction_factor = 4

    @staticmethod
    def are_related(being1: BeingType, being2: BeingType) -> bool:
        ''' Check if the two given beings are related '''
        related = (being1.is_child_of(being2) or being2.is_child_of(being1))
        return related

    def being_is_optimal(self, being: BeingType) -> bool:
        ''' Check if a given being is optimal (i.e. has optimal genetics) '''
        if not being:
            return False
        return all(self.optimal_base is base for base in being.dna)

    def get_population_size(self) -> int:
        ''' Get the number of Beings in the Population '''
        return len(self.population)

    @staticmethod
    def mate(generation, parent1: BeingType, parent2: BeingType) -> BeingType:
        ''' Mate two Beings and return their (singular) offspring '''
        return Being(generation, parent1, parent2)

    def mating_season(self) -> None:
        ''' Invoke mating season (once per generation): non-related Beings randomly mate '''
        # shuffle population to improve randomness
        shuffle(self.population)

        # empty list, storing offspring
        # let n be the current population size, allow kn reproductions
        offspring = [None]*floor(self.reproduction_factor*(len(self.population)))

        for index, child in enumerate(offspring):
            mating_pair = sample(self.population, 2)
            candidate1 = mating_pair[0]
            candidate2 = mating_pair[1]
            if Population.are_related(candidate1, candidate2):
                continue
            offspring[index] = Population.mate(self.generation, candidate1, candidate2)

        # merge offspring array with general population
        offspring = [child for child in offspring if child]
        self.population += offspring

    def test_fitness(self) -> None:
        ''' Impose selection; test fitness. Higher fitness improves survivability '''
        # empty list, storing survivors
        survivors = [None]*len(self.population)

        # test fitness of each member of the population
        for index, being in enumerate(self.population):
            survival_prob = being.get_survival_probability(self.optimal_base, self.generation)
            if random() < survival_prob:
                # being lives
                survivors[index] = being

        # filter dead beings from survivors, set to population
        self.population = [being for being in survivors if being]
        print ("Survived from Gen({} \u2192 {}): {}".format(
            self.generation, self.generation+1, len(self.population)))

    def control_population(self) -> None:
        ''' Dynamic population control: simulate changing environmental pressures '''
        if len(self.population) <= Population.critical_low_pop:
            # increase reproduction rate, halve exp
            self.reproduction_factor += 1
            Being.survival_prob_exponent *= 0.5
        if len(self.population) >= Population.critical_high_pop:
            # halve reproduction rate, double exp
            self.reproduction_factor *= 0.5
            Being.survival_prob_exponent *= 2

    def get_next_gen(self) -> None:
        ''' Simulate one generation: env changes, selection, mating season '''
        self.control_population()
        self.test_fitness()
        if self.get_population_size() > 1:
            self.mating_season()
        self.generation += 1

    def advance_gen(self, count: int) -> None:
        ''' Simulate val(count) number of generations, stop if population dies out '''
        if self.get_population_size() < 1:
            return
        if count <= 0:
            return

        self.get_next_gen()
        print("Gen {} population: {}".format(self.generation, self.get_population_size()))
        if count != 1:
            print("")

        # shuffle population to improve randomness
        shuffle(self.population)

        # recursively call same method, with count decreased
        self.advance_gen(count-1)

    def get_rand_being(self) -> BeingType:
        ''' Get a random Being in the Population '''
        if self.get_population_size() == 0:
            return None
        return choice(self.population)

    def assess_optimality(self) -> None:
        ''' Assess population optimality: does a random Being (in Population) have optimal DNA? '''
        random_being = pop.get_rand_being()
        print("Optimal being: [{}]".format(pop.optimal_base*16))
        if self.being_is_optimal(random_being):
            print("Population is likely optimal\n")
        else:
            print("Population is unlikely optimal\n")

    def print_generation(self) -> None:
        ''' Print each Being in the Population '''
        self.print_subset(self.get_population_size())

    def print_subset(self, count: int) -> None:
        ''' Print a subset of Beings in the Population '''
        if len(self.population) == 0:
            return

        # generate starting and finishing banners
        gen_desc    = "\n=== {} from Generation {} ===\n".format(count, self.generation)
        desc_len    = len(gen_desc) - 2
        gen_end     = "\n{}\n".format("="*desc_len)

        # generate middle string containing subset of beings in population
        pop_string = ""
        left_offset = " "*floor((desc_len - len(self.get_rand_being()))/2)
        for index, being in enumerate(self.population):
            if index >= count:
                break
            if index != 0:
                pop_string += "\n"
            pop_string += left_offset + str(being)

        print(gen_desc + pop_string + gen_end)

    def __init__(self, size: int, optimal_base: str) -> PopType:
        ''' Constructor -> generate Population '''
        if size <= 0:
            print("\nError: Population size must be positive")
            print("Notice: Setting population size to 200")
            size = 200
        if size % 2 != 0:
            size += 1
        self.generation = 0
        self.population = [None] * size
        self.optimal_base = optimal_base
        # for (index, base) in enumerate(self.population):
        for index in range(len(self.population)):
            self.population[index] = Being(self.generation)


# create a population instance with 500 beings
pop = Population(500, choice(Being.dna_bases))
sleep(1)
# print subset of initial population
pop.print_subset(10)

# advance population by n generations, print pop
pop.advance_gen(25)
sleep(1)
pop.print_subset(10)
pop.assess_optimality()
