from __future__ import annotations


HEAT_CELSIUS2KELVIN: float = 273.15


class HeatCapacities:
    Water: float = 4.1813
    Aluminium: float = 0.897


class Heatable:
    Mass: float          # kg
    Temperature: float   # Celsius
    HeatCapacity: float  # kJ / (kg * K)

    def __init__(self, mass: float, temperatureCelsius: float, heatCapacity: float):
        self.Mass = mass
        self.Temperature = temperatureCelsius
        self.HeatCapacity = heatCapacity

    def CalculateHeatEnergy(self, deltaK: float) -> float:
        return self.HeatCapacity * self.Mass * deltaK  # E = c * m * dK | (Spesifikk varmekapasitet likning)

    def CalculateDeltaK(self, heatEnergy: float) -> float:
        return heatEnergy / (self.Mass * self.HeatCapacity)  # dK = E / (c * m) | (Reformulert spesifikk varmekapasitet likning)

    def AddHeatEnergy(self, heatEnergy: float) -> None:
        self.Temperature += self.CalculateDeltaK(heatEnergy)

    def TransferHeatEnergy(self, other: Heatable, virkingsGrad: float) -> None:
        temperatureDifference: float = self.Temperature - other.Temperature  # Sjekker etter definisjonen av varme (Q) om vi kan overføre varmeenergi til "other" systemet

        if temperatureDifference > 0:
            heatEnergyToTransfer: float = self.CalculateHeatEnergy(temperatureDifference) * virkingsGrad
            heatCapacityRatio: float = 1 + (other.HeatCapacity * other.Mass) / (self.HeatCapacity * self.Mass)
            heatTransferred: float = heatEnergyToTransfer - heatEnergyToTransfer / heatCapacityRatio

            self.Temperature -= self.CalculateDeltaK(heatTransferred)    # Vi tar bort mengden varme som vi kan ta bort før en av de ulike systemene får større eller mindre varme enn den andre
            other.AddHeatEnergy(heatTransferred)                         # Perfekt umiddelbar varmeenergi overføring antatt her!
