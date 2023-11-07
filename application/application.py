class Application:
    def __init__(self, id, dependencies = []):
        self.id = id
        self.dependencies = dependencies

    def get_dependencies(self):
        return self.dependencies
    
    def set_proxy(self, proxy):
        self.proxy = proxy

    async def process(self, request):
        raise Exception('Not implemented')