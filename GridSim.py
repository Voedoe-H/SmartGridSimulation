import numpy as np
import matplotlib.pyplot as plt


class SmartGrid:
    """ Very Primitive Model for a smart Grid """

    def __init__(self, V_min=210, V_max=230, a=0.05, b=220, c=0.2, d=0.2, dt=0.01, T=100, inputs=None):
        """ 
            V_min: minimal voltage of the grid, acts as decision boundary to move into the undervoltage state
            V_max: maximal voltage of the grid, acts as decision boundary to move into the overvoltage state
            a: rate of change of the voltage in normal state
            b: baseline voltage
            c: rate of change in the overvoltage state
            d: rate of change in the undervoltage state
            dt: time step length assumed to be in s
            T: num time steps dt in the overall simualtion
            inputs: External input functions acting on the state of the system V
        """
        self.V_min = V_min
        self.V_max = V_max
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.dt = dt
        self.T = T
        self.inputs = inputs if inputs else []
        self.reset()

    def apply_inputs(self, t):
        for input_func in self.inputs:
            self.V += input_func(t)

    def reset(self):
        self.V = 220  # Initial voltage
        self.state = 'Q1'  # Start in normal state
        self.time = np.arange(0, self.T, self.dt)
        self.voltage = []

    def normal_state(self):
        self.V += (-self.a * self.V + self.b) * self.dt

    def overvoltage_state(self):
        self.V += -self.c * (self.V - self.V_max) * self.dt

    def undervoltage_state(self):
        self.V += self.d * (self.V_min - self.V) * self.dt

    def simulate(self):
        self.reset()
        for t in self.time:

            self.apply_inputs(t)

            if self.state == 'Q1':  # Normal operation
                self.normal_state()
                if self.V > self.V_max:
                    self.state = 'Q2'
                elif self.V < self.V_min:
                    self.state = 'Q3'
            elif self.state == 'Q2':  # Overvoltage
                self.overvoltage_state()
                if self.V_min <= self.V <= self.V_max:
                    self.state = 'Q1'
            elif self.state == 'Q3':  # Undervoltage
                self.undervoltage_state()
                if self.V_min <= self.V <= self.V_max:
                    self.state = 'Q1'
            
            self.voltage.append(self.V)
    
    def plot_results(self):
        plt.figure(figsize=(10, 6))
        plt.plot(self.time, self.voltage, label='Voltage (V)')
        plt.axhline(self.V_min, color='r', linestyle='--', label='V_min')
        plt.axhline(self.V_max, color='g', linestyle='--', label='V_max')
        plt.title('Smart Grid Voltage Control Simulation')
        plt.xlabel('Time (s)')
        plt.ylabel('Voltage (V)')
        plt.legend()
        plt.grid(True)
        plt.show()


def random_fluctuation(t):
    return np.random.normal(0, 0.5)

def periodic_disturbance(t):
    return 5 * np.sin(2 * np.pi * t / 50)

def step_change(t):
    return 10 if 20 <= t <= 40 else 0

inputs = [random_fluctuation, periodic_disturbance, step_change]

grid = SmartGrid(inputs=inputs)
grid.simulate()
grid.plot_results()