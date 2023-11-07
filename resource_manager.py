class ResourceManager:
    def __init__(self, cpu, memory, storage):
        self.cpu_limit = cpu
        self.memory_limit = memory
        self.storage_limit = storage

        self.cpu = 0
        self.memory = 0
        self.storage = 0

    def reserve_cpu(self, cpu):
        # print(f'current: {self.cpu}, request: {cpu}, limit: {self.cpu_limit}')
        if self.cpu + cpu > self.cpu_limit:
            return False

        self.cpu += cpu
        return True
    
    def release_cpu(self, cpu):
        self.cpu -= cpu

        