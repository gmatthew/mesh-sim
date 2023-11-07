from logger import Logger

class ResourceManager:
    def __init__(self, cpu, memory, storage):
        super().__init__()
        self.cpu_limit = cpu
        self.memory_limit = memory
        self.storage_limit = storage

        self.cpu = 0
        self.memory = 0
        self.storage = 0

    def reserve_cpu(self, cpu):
        if self.cpu + cpu > self.cpu_limit:
            return False

        self.cpu += cpu
        return True
    
    def release_cpu(self, cpu):
        self.cpu -= cpu

        