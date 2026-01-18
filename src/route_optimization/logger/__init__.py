class Logger:
    def __init__(self) -> None:
        self.counts = []
        self.values = []
        self.parameters = []
        self.iter = 0

    def update(self, xk):
        self.iter += 1
        self.parameters.append(xk)

    def register_energy(self, energy):
        self.values.append(energy)
        self.counts.append(len(self.values))
