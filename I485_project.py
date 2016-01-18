
import random, string, numpy, time
from turtle import *

def init():
   
    # Create an empty population
    pop = []
   
    for i in range(pop_size):
        genotype = ''.join(random.choice(['F','+F', '-F']) for x in range(genotype_size))
        pop.append(genotype)
   
    return(pop)
    
def DOL_system(axiom,p,max_it):
    words = list(axiom)
    t = 1
    
    while t <= max_it:
        rs = []
        
        for word in words:
            if word in p.keys():
                rs = rs + list(p[word])
            else:
                rs = rs + list(word)   
        words = rs
        t = t + 1
    return ''.join(words)
    

def evaluate(pop):
    
    fitness = []
    
    for i in range(pop_size):
        
        genotype = DOL_system('F',{'F':pop[i]},iterations)

        fitness_value = 0
        
        if body_pressure() != 0 and social_pressure() != 0:
            
            rate1 = (body_pressure()/1.0)/(social_pressure()/1.0) 
            
        elif body_pressure() > social_pressure():
            
            rate1 = 10000.0
            
        else: rate1 = 0.0
        
        if genotype.count('-') != 0 and genotype.count('+') != 0:
            
            rate2 = (genotype.count('-')/1.0)/(genotype.count('+')/1.0)
        elif genotype.count('-') > genotype.count('+'):
            rate2 = 10000.0
        else: rate2 = 0.0
         #'-' represent body pressure, '+' represent social pressure
         
        fitness_value += 1/(abs(rate1-rate2)+0.00001) #compare the difference between two rate, the closer rate, the higher fitness
        fitness_value += genotype.count('F') * 3
        
        fitness.append(fitness_value)
    
    fitness = [f * 1.0/sum(fitness) for f in fitness]
    
    return(fitness)

def select(fitness, pop):
    
    # Select first parent
    parent_1_index = -9999  #indicates that parent_1 is yet to be chosen
    cumulated_fitness = 0
    roulette_marker = random.random()  #indicates that the 'roulette wheel' has settled on a random number
    for i in range(pop_size):
        cumulated_fitness += fitness[i]
        if cumulated_fitness >= roulette_marker:
            parent_1_index = i
            break
    
    # Select second parent different from the first parent
    parent_2_index = parent_1_index  #indicates that parent_2 is yet to be chosen
    while parent_2_index == parent_1_index:  #this ensures that the two parents chosen are distinct
        cumulated_fitness = 0
        roulette_marker = random.random()  #indicates that the 'roulette wheel' has settled on a random number
        for i in range(pop_size):
            cumulated_fitness += fitness[i]
            if cumulated_fitness >= roulette_marker:
                parent_2_index = i
                break
    
    return([pop[parent_1_index], pop[parent_2_index]])
    

# Recombine two parents to produce two offsprings, with a certain probability
# specified by recombination_rate
def recombine(parent_1, parent_2, recombination_rate):
   
    r = random.random()
   
    if r <= recombination_rate:  
        #recombine
        slice_point = random.randint(0, genotype_size-1)
        offspring_1 = parent_1[0 : slice_point] + parent_2[slice_point : genotype_size]
        offspring_2 = parent_2[0 : slice_point] + parent_1[slice_point : genotype_size]
        return([offspring_1, offspring_2])
   
    else:  #don't recombine
        return([parent_1, parent_2])


def mutate(genotype, mutation_rate):
   
    mutated_genotype = genotype  #indicates that the genotype is yet to be mutated
   
    for i in range(genotype_size):
   
        r = random.random()
   
        if r <= mutation_rate:  
            
            new_symbol = random.choice(['F','+', '-'])
            
            mutated_genotype = mutated_genotype[0 : i] + new_symbol + mutated_genotype[(i+1) : genotype_size]

    return(mutated_genotype)


def initturtle():
        
        pencolor('blue')
        
        speed('fastest')
        
        tracer(1)
        
        degrees()
        
        goto(0,0)
        
        pendown()


def graphword(str):

        for char in str:

            if char == 'F':
                
                forward(3)


            if char == '-':
                
                left(70)
                
            if char == '+':
                
                right(70)


cig = 0
achol = 0 
workout = 0 
sleep = 0
rel = ''

# EXAMPLE GA parameers
def body_pressure():
    result = 1+ cig * 2 \
        + achol * 8 \
        - workout * 2 \
        + (8 - sleep) * 2 #assume the healthy sleep hours is 8 horus
    return result
    
def social_pressure():

    result = 1 - cig * 3 \
        + achol * 6 \
        - workout  #smoking is somehow reduce the social pressure
    if rel == "yes":
        result += 8
    
    return result



pop_size = 20
num_generations = 30
genotype_size = 6
iterations = 4

total_pressure = social_pressure() + body_pressure()
recombination_rate = social_pressure() / total_pressure
mutation_rate = body_pressure() / total_pressure



    
        

pop = init()


             
        

if __name__ == "__main__":
    
    cig += input("Please enter how many cigs do you smoke per day: ")
    achol = input("Please enter how many times do you drink achole per week: ")
    workout = input("Please enter how many hours do you spend in sports per week: ")
    sleep = input("Please enter how many hours do you sleep every day: ")
    rel = input("Are you in a relationship? (yes/no): ")
    
    

    
    
     
                    
    for gen in range(num_generations):

   	fitness = evaluate(pop)
   	new_pop = []  
        best = []
        while (len(new_pop) < pop_size):  

              		[parent_1, parent_2] = select(fitness, pop)

          		[offspring_1, offspring_2] = recombine(parent_1, parent_2, recombination_rate)

          		mutated_genotype_1 = mutate(offspring_1, mutation_rate)
          		mutated_genotype_2 = mutate(offspring_2, mutation_rate)
		
          		new_pop.append(mutated_genotype_1)
          		new_pop.append(mutated_genotype_2)
      		
        pop = new_pop 
   	
        best_geno = pop[numpy.argmax(evaluate(pop))]
	
        best_value = (max(evaluate(pop)))

        if best == []:
                    best = [best_geno,best_value]
        elif best_value > best[1]:
                    best = [best_geno,best_value]
        print best_geno
    
        initturtle()          

        stack = list()

        graph = DOL_system('F',{'F':best[0]},iterations)

        graphword(graph)

        done()