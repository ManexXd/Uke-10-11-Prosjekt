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

time: float = 0.0                # s
kokePlateEffekt: float = 1.500   # kW
# Total varmetap: (4.1813 * 1.50 * (70.94377914704616-20.5)) / 0.87883572394 - (4.1813 * 1.50 * (35.9-20.5)) / 0.87883572394 = 250kJ
# Prosent varmeenergi fra kokeplate som må gå bort: 250kJ/360kJ = 0.694


# Derivert regresjonsfunksjon fra et regneark i geogebra. X = tid & Y = deltaEnergiSimulasjon - deltaEnergiForsøk
def Warmetap(t: float) -> float:
    return 1/5000000000000 * (-22358711674*t + 7873113785579)


# Main simulation loop
while time < SIMULATION_ENDTIME:
    kettle.AddHeatEnergy((kokePlateEffekt - Warmetap(time)) * SIMULATION_DELTATIME)  # Overføring av varmeenergi fra kokeplaten til kasserollen (kJ / s * s = kJ)
    kettle.TransferHeatEnergy(water, 1.0)                          # Overføring av varmeenergi fra kasserollen over til vannet

    simulationTemperatureData.append(water.Temperature)           # Legger til gradvis alle kalkulerte vanntemperaturer til simulasjons temperatur listen
    simulationTimeData.append(time)                               # Legger til gradvis alle simulasjons tidspunktene til simulasjons tid listen

    time += SIMULATION_DELTATIME                                  # Tid inkrementering etter delta tid


# print(realTemperatureData[int(SIMULATION_ENDTIME*2)-1], (HeatCapacities.Water * water.Mass * (water.Temperature - 20.5)) / 0.87883572394 - (HeatCapacities.Water * water.Mass * (realTemperatureData[int(SIMULATION_ENDTIME*2)-1] - 20.5)) / 0.87883572394)


# Plotting
pyplot.subplot(1, 3, 1)
pyplot.plot(realTimeData, realTemperatureData)
pyplot.xlabel("Tid (s)")
pyplot.ylabel("Temperatur (°C)")
pyplot.title("Forsøk vann temperatur")

pyplot.subplot(1, 3, 2)
pyplot.plot(simulationTimeData, simulationTemperatureData)
pyplot.xlabel("Tid (s)")
pyplot.ylabel("Temperatur (°C)")
pyplot.title("Simulasjon vann temperatur")

pyplot.subplot(1, 3, 3)
pyplot.plot(simulationTimeData, simulationTemperatureData, color="Blue")
pyplot.plot(realTimeData, realTemperatureData, color="Red")
pyplot.legend(["Blå: Simulasjon", "Rød: Forsøk"]);
pyplot.xlabel("Tid (s)")
pyplot.ylabel("Temperatur (°C)")
pyplot.title("Simulasjons & Forsøk vann temperatur")

pyplot.show()
