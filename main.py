from Heatable import Heatable, HeatCapacities
from matplotlib import pyplot
from numpy import *


# Simulation Constants
SIMULATION_DELTATIME: float = 0.5  # s
SIMULATION_ENDTIME: float = 240.0  # s

# Simulation values
waterTemperatureData: ndarray = loadtxt("datafil.txt")
realTemperatureData: ndarray = waterTemperatureData[:, 1]
realTimeData: ndarray = waterTemperatureData[:, 0]

water: Heatable = Heatable(1.50, 20.5, HeatCapacities.Water)
kettle: Heatable = Heatable(0.964, 20.5, HeatCapacities.Aluminium)

simulationTemperatureData: list = []
simulationTimeData: list = []

time: float = 0.0             # s
kokePlateEffekt: float = 1.5  # kJ / s
varmeTap: float = -1.0422     # kJ / s


# Main simulation loop
print(water.Temperature, kettle.Temperature)

while time < SIMULATION_ENDTIME:
    kettle.AddHeatEnergy(kokePlateEffekt * SIMULATION_DELTATIME)
    kettle.AddHeatEnergy(varmeTap * SIMULATION_DELTATIME)
    kettle.TransferHeatEnergy(water)

    simulationTemperatureData.append(water.Temperature)
    simulationTimeData.append(time)

    time += SIMULATION_DELTATIME

print(water.Temperature, kettle.Temperature)


# Plotting
pyplot.subplot(1, 3, 1)
pyplot.plot(realTimeData, realTemperatureData)
pyplot.xlabel("Tid (s)")
pyplot.ylabel("Temperatur (°C)")
pyplot.title("Ekte temperatur til vann etter tid")

pyplot.subplot(1, 3, 3)
pyplot.plot(simulationTimeData, simulationTemperatureData)
pyplot.xlabel("Tid (s)")
pyplot.ylabel("Temperatur (°C)")
pyplot.title("Simulasjons temperatur til vann etter tid")

pyplot.show()
