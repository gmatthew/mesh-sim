from pod import Pod

# Service is a collection of pods
class Service:
    def __init__(self, name):
        self.name = name
        self.pods = []

    def attach_pod(self, pod):
        self.pods.append(pod)

    def get_pods(self):
        return self.pods   
    