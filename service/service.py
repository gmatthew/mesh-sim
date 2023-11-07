from pod import Pod
from logger import Logger
# Service is a collection of pods
class Service(Logger):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.pods = []

    def attach_pod(self, pod):
        self.pods.append(pod)

    def get_pods(self):
        return self.pods   
    