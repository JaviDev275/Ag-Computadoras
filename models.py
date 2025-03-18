from copy import deepcopy

class CPU:
    def __init__(
        self,
        maker: str,
        model: str,
        performance: int,
        price: float,
        power_consumption: int,
        has_integrated_graphics: bool = False,
        integrated_graphics_power: int = 0,
    ) -> None:
        self.maker: str = maker
        self.model: str = model
        self.performance: int = performance
        self.price: float = price
        self.power_consumption: int = power_consumption
        self.has_integrated_graphics: bool = has_integrated_graphics
        self.integrated_graphics_power: int = integrated_graphics_power

    def __deepcopy__(self, memo):
        return CPU(
            self.maker,
            self.model,
            self.performance,
            self.price,
            self.power_consumption,
            self.has_integrated_graphics,
            self.integrated_graphics_power,
        )

    def __str__(self):
        return f"CPU: {self.maker} {self.model}, performance: {self.performance}, Price: ${self.price}"


class GPU:
    def __init__(
        self, maker: str, price: float, power_consumption: int,power: int
    ) -> None:
        self.maker: str = maker
        self.price: float = price
        self.power_consumption: int = power_consumption
        self.power: int = power

    def __deepcopy__(self, memo):
        return GPU(
            self.maker, self.price, self.power_consumption,self.power
        )

    def __str__(self):
        return (
            f"GPU: {self.maker}, Price: ${self.price}"
        )


class RAM:
    def __init__(
        self,
        maker: str,
        model: str,
        capacity: int,
        frequency: int,
        type: str,
        price: float,
    ) -> None:
        self.maker: str = maker
        self.model: str = model
        self.capacity: int = capacity
        self.frequency: int = frequency
        self.type: str = type
        self.price: float = price

    def __str__(self):
        return f"RAM: {self.maker} {self.model}, Capacity: {self.capacity}GB, Frequency: {self.frequency}MHz, Type: {self.type}, Price: ${self.price}"


class Storage:
    def __init__(
        self, maker: str, model: str, type: str, capacity: float,price: float
    ) -> None:
        self.maker: str = maker
        self.model: str = model
        self.type: str = type
        self.capacity: float = capacity
        self.price: float = price

    def __str__(self):
        return f"Storage: {self.maker} {self.type} {self.capacity}GB, Price: ${self.price}"


class Motherboard:
    def __init__(
        self,
        maker: str,
        model: str,
        price: float,
        power_consumption: int,
        max_ram_capacity: int,
        max_ram_frequency: int,
        ram_socket_type: str,
        compatible_cpus: list[CPU],
    ) -> None:
        self.maker: str = maker
        self.model: str = model
        self.price: float = price
        self.max_ram_capacity: int = max_ram_capacity
        self.max_ram_frequency: int = max_ram_frequency
        self.ram_socket_type: str = ram_socket_type
        self.power_consumption = power_consumption

        self.compatible_cpus: list[CPU] = compatible_cpus

    def is_cpu_compatible(self, cpu: CPU) -> bool:
        try:
            compatible: bool = cpu.model in [
                compatible_cpu.model for compatible_cpu in self.compatible_cpus
            ]
            return compatible
        except Exception:
            # print(cpu)
            return False

    def is_ram_compatible(self, ram: RAM) -> bool:
        return (
            ram.type == self.ram_socket_type
            and ram.frequency <= self.max_ram_frequency
            and ram.capacity <= self.max_ram_capacity
        )

    def __deepcopy__(self, memo):
        return Motherboard(
            self.maker,
            self.model,
            self.price,
            self.power_consumption,
            self.compatible_cpus,
            self.max_ram_capacity,
            self.max_ram_frequency,
            self.ram_socket_type,
        )

    def __str__(self):
        return f"Motherboard: {self.maker} {self.model}, Price: ${self.price}"


class PSU:
    def __init__(self, maker: str, model: str, capacity: int, price: float) -> None:
        self.maker: str = maker
        self.model: str = model
        self.capacity: str = capacity
        self.price: float = price

    def __deepcopy__(self, memo):
        return PSU(self.maker, self.model, self.capacity, self.price)

    def __str__(self) -> str:
        return f"PSU: {self.maker} {self.model}, capacity: {self.capacity}W, price: {self.price}"


class Computer:
    def __init__(
        self,
        cpu: CPU,
        gpu: GPU | None,
        ram: RAM,
        storage: Storage,
        motherboard: Motherboard,
        psu: PSU,
        fitness: float = 0
    ) -> None:
        self.cpu: CPU = cpu
        self.gpu: GPU | None = gpu
        self.ram: RAM = ram
        self.storage: Storage = storage
        self.motherboard: Motherboard = motherboard
        self.psu: PSU = psu
        # Ajuste aquí para manejar el caso de la GPU siendo None
        self.price: float = (
            self.cpu.price
            + (self.gpu.price if self.gpu else 0) 
            + self.ram.price
            + self.storage.price
            + self.motherboard.price
            + self.psu.price
        )
        self.fitness = fitness


    def __str__(self):
        return f"Computer Configuration:\n{str(self.cpu)}\n{str(self.gpu)}\n{str(self.ram)}\n{str(self.storage)}\n{str(self.motherboard)}\n{str(self.psu)}\nTotal Price: ${self.price}"

    def __deepcopy__(self, memo):
        new_computer = Computer(
            deepcopy(self.cpu),
            deepcopy(self.gpu),
            deepcopy(self.ram),
            deepcopy(self.storage),
            deepcopy(self.motherboard),
            deepcopy(self.psu),
        )

        new_computer.price = self.price
        return new_computer

    def is_psu_capacity_enough(self) -> bool:
        power_needed = self.cpu.power_consumption + (self.gpu.power_consumption if self.gpu else 0) + self.motherboard.power_consumption + 50
        return (power_needed < self.psu.capacity) and (
            self.psu.capacity - power_needed <= 50
        )
        
    def is_bottleneck(self) -> bool:
        if self.gpu is None:
            gpu_power = 0
        else:
             gpu_power = self.gpu.power
        
        bottleneck = self.cpu.performance - gpu_power
        return (bottleneck <= 20)
    
    def points_for_relation_quality_cpu(self) -> float:
        relation=(self.cpu.performance/self.cpu.price)*100
        return relation
    
    def points_for_relation_quality_gpu(self) -> float:
        if self.gpu is None:
            return 0  # Si no hay GPU, la relación es 0
        else:
            gpu_power = self.gpu.power
            gpu_price = self.gpu.price
            if gpu_price == 0:
                return 0 
            else:
                relation = (gpu_power / gpu_price) * 650
                return relation



class UserPreferences:
    def __init__(self, min_price: int, max_price: int, usage: str) -> None:
        self.min_prince: int = min_price
        self.max_price: int = max_price
        self.usage: str = usage
