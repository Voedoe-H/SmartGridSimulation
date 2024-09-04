import numpy as np
import matplotlib.pyplot as plt

# Parameters
V_min = 210  # Minimum voltage (V)
V_max = 230  # Maximum voltage (V)
a = 0.05  # Decay rate in normal state
b = 220  # External input in normal state
c = 0.2  # Correction rate for overvoltage
d = 0.2  # Correction rate for undervoltage
dt = 0.01  # Time step
T = 100  # Total simulation time

# Initial conditions
V = 220  # Initial voltage
state = 'Q1'  # Start in normal state
time = np.arange(0, T, dt)
voltage = []

# Simulation loop
for t in time:
    if state == 'Q1':  # Normal operation
        V += (-a * V + b) * dt
        if V > V_max:
            state = 'Q2'
        elif V < V_min:
            state = 'Q3'
    elif state == 'Q2':  # Overvoltage
        V += -c * (V - V_max) * dt
        if V_min <= V <= V_max:
            state = 'Q1'
    elif state == 'Q3':  # Undervoltage
        V += d * (V_min - V) * dt
        if V_min <= V <= V_max:
            state = 'Q1'
    
    voltage.append(V)

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(time, voltage, label='Voltage (V)')
plt.axhline(V_min, color='r', linestyle='--', label='V_min')
plt.axhline(V_max, color='g', linestyle='--', label='V_max')
plt.title('Smart Grid Voltage Control Simulation')
plt.xlabel('Time (s)')
plt.ylabel('Voltage (V)')
plt.legend()
plt.grid(True)
plt.show()