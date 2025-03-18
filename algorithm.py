from copy import deepcopy
from statistics import mean
from data import cpus, gpus, rams, storages, motherboards, psus
from models import CPU, GPU, PSU, RAM, Computer, Motherboard, Storage, UserPreferences
import random


class ComputerGenerator:
    def __init__(
        self,
        population_size: int,
        crossover_rate: float,
        mutation_rate: float,
        generations: int,
        user_preferences: UserPreferences,
    ) -> None:
        self.population_size: int = population_size
        self.crossover_rate: float = crossover_rate
        self.mutation_rate: float = mutation_rate
        self.generations: int = generations

        self.population: list[Computer] = []
        self.user_preferences: UserPreferences = user_preferences

        self.best_cases = []
        self.avg_cases = []
        self.worst_cases = []

    def generate_initial_population(self) -> None:
        for _ in range(self.population_size):
            cpu: CPU = random.choice(cpus)
            gpu: GPU = random.choice(gpus)
            ram: RAM = random.choice(rams)
            storage: Storage = random.choice(storages)
            motherboard: Motherboard = random.choice(motherboards)
            psu: PSU = random.choice(psus)
            
            computer = Computer(cpu, gpu, ram, storage, motherboard, psu)
            
            fitness = self.fitness_function(computer)
            
            computer.fitness = fitness
            
            self.population.append(computer)

    def fitness_function(self, computer: Computer) -> int:
        """
            Evalua la aptitud de un genotipo (computadora) tomando en cuenta los siguiente:
            - El precio total de la computadora está dentro rango de precio elegido por el usuario.
            - Los componentes son compatiables
            - La capacidad de la PSU es suficiente, pero tampoco excesiva.
            - Los componentes de la computadora corresponden a las necesarias para el tipo de uso seleccionado
              de la computadora
        Returns:
            int: Aptitud de la computadora (genotipo)
        """
        fitness_score: int = 0

        fitness_score += 30 if self.is_within_price_range(computer) else 0

        fitness_score += 30 if self.all_components_are_compatible(computer) else 0

        fitness_score += self.get_usage_score(computer)

        fitness_score += 10 if computer.is_psu_capacity_enough() else 0
        
        fitness_score += 10 if computer.is_bottleneck() else 0
                
        fitness_score += computer.points_for_relation_quality_cpu()
        
        fitness_score += computer.points_for_relation_quality_gpu()


        return fitness_score

    def is_within_price_range(self, computer: Computer) -> bool:
        return (
            self.user_preferences.min_prince
            <= computer.price
            <= self.user_preferences.max_price
        )
        
    def all_components_are_compatible(self, computer: Computer) -> bool:
        return all(
            [
                computer.motherboard.is_cpu_compatible(computer.cpu),
                computer.motherboard.is_ram_compatible(computer.ram),
            ]
        )

    def get_usage_score(self, computer: Computer) -> int:
        primary_usage_score: int = 0

        match (self.user_preferences.usage):
            case "ofimática":
                primary_usage_score = self.get_ofimatica_score(computer)
            case "juegos":
                primary_usage_score = self.get_gaming_score(computer)
            case "diseño gráfico":
                primary_usage_score = self.get_graphics_design_score(computer)
            case "edición de video":
                primary_usage_score = self.get_video_editing_score(computer)
            case "navegación web":
                primary_usage_score = self.get_web_navigation_score(computer)
            case "educación":
                primary_usage_score = self.get_education_score(computer)
            case "arquitectura":
                primary_usage_score = self.get_architecture_score(computer)
            case _:
                primary_usage_score = 0

        return primary_usage_score

    def get_education_score(self, computer: Computer):
        if (
            30 <= computer.cpu.performance <= 60
            and computer.ram.capacity > 8 and computer.ram.capacity <= 16
            and computer.storage.type == "SSD"
            and computer.storage.capacity > 128 and computer.storage.capacity <= 500
            and ((computer.gpu != None and computer.gpu.power < 40) or (computer.cpu.has_integrated_graphics and computer.cpu.has_integrated_graphics < 60))
        ):
            return 30
        return 0

    def get_web_navigation_score(self, computer: Computer):
        if (
            10 <= computer.cpu.performance <= 30
            and computer.ram.capacity == 8
            and computer.storage.type == "SSD"
            and computer.storage.capacity < 500
            and computer.gpu == None
            and computer.cpu.integrated_graphics < 20
        ):
            return 30
        return 0

    def get_video_editing_score(self, computer: Computer):
        if (
            computer.gpu is not None
            and computer.gpu.power >= 30
            and computer.ram.capacity >= 32
            and computer.storage.capacity > 1_000
            and computer.storage.type == "SSD"
        ):
            return 30
        return 0

    def get_graphics_design_score(self, computer: Computer):
        if (
            computer.gpu is not None
            and computer.gpu.power >= 30
            and computer.ram.capacity >= 16
            and computer.storage.capacity > 1_000
            and computer.storage.type == "SSD"
        ):
            return 30
        return 0

    def get_gaming_score(self, computer: Computer):
        if (
            computer.gpu is not None
            and computer.gpu.power>= 50
            and computer.ram.capacity >= 16
            and computer.cpu.performance >= 64
            and computer.storage.type == "SSD"
        ):
            return 30
        return 0

    def get_ofimatica_score(self, computer: Computer):
        if (
            computer.cpu.performance >= 10
            and computer.ram.capacity >= 8
            and computer.storage.capacity > 500
            and computer.gpu is not None and computer.gpu.power< 30
        ):
            return 30
        return 0

    def get_architecture_score(self, computer: Computer):
        if (
            computer.gpu is not None
            and computer.cpu.performance >= 60
            and computer.gpu.power >= 60
            and computer.ram.capacity >= 32
            and computer.storage.capacity > 1_000
            and computer.storage.type == "SSD"
        ):
            return 30
        return 0

    def crossover(
        self, parent1: Computer, parent2: Computer
    ) -> tuple[Computer, Computer]:
        new_computer1 = Computer(
            cpu=parent1.cpu,
            gpu=parent2.gpu,
            ram=parent1.ram,
            storage=parent2.storage,
            motherboard=parent1.motherboard,
            psu=parent2.psu,
        )
        new_computer2 = Computer(
            cpu=parent2.cpu,
            gpu=parent1.gpu,
            ram=parent2.ram,
            storage=parent1.storage,
            motherboard=parent2.motherboard,
            psu=parent1.psu,
        )

        return new_computer1, new_computer2

    def pruning(self):
        self.population = sorted(self.population, key=lambda x: x.fitness, reverse=True)
        
        self.population = self.population[: self.population_size]

    def mutate(self, computer: Computer) -> Computer:
        mutated_computer = deepcopy(computer)

        if random.uniform(0, 1) < self.mutation_rate:
            mutated_computer.cpu = random.choice(cpus)

        if random.uniform(0, 1) < self.mutation_rate:
            mutated_computer.gpu = random.choice(gpus + [None])

        if random.uniform(0, 1) < self.mutation_rate:
            mutated_computer.ram = random.choice(rams)

        if random.uniform(0, 1) < self.mutation_rate:
            mutated_computer.storage = random.choice(storages)

        if random.uniform(0, 1) < self.mutation_rate:
            mutated_computer.motherboard = random.choice(motherboards)

        return mutated_computer

    def run(self) -> Computer:
        self.generate_initial_population()

        for _ in range(self.generations):
            children = []
            for i in range(0, self.population_size - 1, 2):
                parent1, parent2 = self.population[i], self.population[i + 1]
                if random.uniform(0, 1) < self.crossover_rate:
                    child1, child2 = self.crossover(parent1, parent2)
                    children.extend([child1, child2])

            children = [self.mutate(computer) for computer in children]
            
            # calcular fitness de los nuevos individuos
            for indiv in children:
                fitness = self.fitness_function(indiv)
                indiv.fitness = fitness

            self.population.extend(children)
            
            fitness_scores = sorted(self.population, key=lambda x: x.fitness, reverse=True)
            
            self.best_cases.append(fitness_scores[0])
            print(f"mejor score: ${fitness_scores[0].fitness}")
            # sum(persona.fitness for persona in personas_ordenadas) / len(personas_ordenadas)
            self.avg_cases.append(sum(computer.fitness for computer in self.population)/len(self.population))
            self.worst_cases.append(fitness_scores[-1])

            #if len(self.population) > self.population_size:
            self.pruning()

            ("Last gene:")
        for computer in self.population:
            pass
            (computer)
        best_computer = max(
            self.population, key=lambda computer: self.fitness_function(computer)
        )
        return best_computer
