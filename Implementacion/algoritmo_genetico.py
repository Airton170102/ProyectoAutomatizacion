from concurrent.futures import ThreadPoolExecutor
import random

class GeneticAlgorithm:
    """Clase que implementa un algoritmo genético optimizado para parámetros PID."""

    def __init__(self, objective_function, population_size, chromosome_size, gene_bounds, mutation_probability,
                 crossover_probability, crossover_rate):
        self.objfunction = objective_function
        self.population_size = population_size
        self.chromosome_size = chromosome_size
        self.gene_bounds = gene_bounds
        self.mutation_probability = mutation_probability
        self.crossover_probability = crossover_probability
        self.crossover_rate = crossover_rate
        self.population = self.inicializar_poblacion()
        self.fitness_cache = {}  # Diccionario para memoization

    def inicializar_poblacion(self):
        """Inicializa la población aleatoria dentro de los rangos específicos para cada gen."""
        return [
            [random.uniform(self.gene_bounds[i][0], self.gene_bounds[i][1]) for i in range(self.chromosome_size)]
            for _ in range(self.population_size)
        ]


    def evaluar_fitness(self, individuo):
        """Evalúa el fitness de un individuo con memoization."""
        key = tuple(individuo)
        if key in self.fitness_cache:
            return self.fitness_cache[key]
        fitness = 1 / (self.objfunction(individuo) + 1e-6)
        self.fitness_cache[key] = fitness
        return fitness

    def evaluar_fitness_poblacion(self):
        """Evalúa el fitness de toda la población en paralelo."""
        with ThreadPoolExecutor() as executor:
            fitness_poblacion = list(executor.map(self.evaluar_fitness, self.population))
        return fitness_poblacion

    def seleccionar(self):
        """Selecciona dos individuos usando selección proporcional al fitness."""
        fitness = self.evaluar_fitness_poblacion()
        total_fitness = sum(fitness)
        probabilidades = [f / total_fitness for f in fitness]
        return random.choices(self.population, weights=probabilidades, k=2)

    def cruzar(self, padre1, padre2):
        """Cruza de un solo punto entre dos padres."""
        if random.random() < self.crossover_probability:
            punto = random.randint(1, self.chromosome_size - 1)
            hijo1 = padre1[:punto] + padre2[punto:]
            hijo2 = padre2[:punto] + padre1[punto:]
            return hijo1, hijo2
        return padre1, padre2

    def mutar(self, individuo):
        """Muta un individuo respetando los límites específicos para cada gen."""
        for i in range(len(individuo)):
            if random.random() < self.mutation_probability:
                individuo[i] = random.uniform(self.gene_bounds[i][0], self.gene_bounds[i][1])
        return individuo


    def optimizar(self, generaciones):
        """Optimiza los parámetros PID usando el algoritmo genético."""
        no_mejora = 0
        mejor_fitness_anterior = None

        for gen in range(generaciones):
            # Evaluar fitness de la población
            fitness_poblacion = self.evaluar_fitness_poblacion()
            mejor_fitness = max(fitness_poblacion)
            mejor_individuo = self.population[fitness_poblacion.index(mejor_fitness)]

            # Imprimir información de la generación
            print(f"Generación {gen + 1}:")
            print(f"  Mejor individuo: {mejor_individuo}")
            print(f"  Mejor fitness: {mejor_fitness:.6f}\n")


            # Crear nueva población
            nueva_poblacion = []
            for _ in range(self.population_size // 2):
                padre1, padre2 = self.seleccionar()
                hijo1, hijo2 = self.cruzar(padre1, padre2)
                nueva_poblacion.append(self.mutar(hijo1))
                nueva_poblacion.append(self.mutar(hijo2))
            self.population = nueva_poblacion

        # Retornar el mejor individuo final
        return max(self.population, key=self.evaluar_fitness)
