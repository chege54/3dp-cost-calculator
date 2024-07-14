from pint_units import Q_
from parameters import CostParameters
from machine_db import Machines
from material_db import Materials

class FixCost:
    '''
        Cost is a class that represents the one time costs.
    '''
    def __init__(self, name, x:Q_) -> None:
        self.name = name
        self.value = x


class ProportionalCost:
    '''
        Cost is a class that represents the proportional costs.
    '''
    def __init__(self, name, cost_per_1:Q_, x:Q_) -> None:
        self.name = name
        self.cost_per_x = cost_per_1
        self.value = cost_per_1 * x


class ManualCost(ProportionalCost):
    '''

    '''
    def __init__(self, name: Q_, x: Q_) -> None:
        super().__init__(name=name, cost_per_1=CostParameters.manual_cost_per_hour, x=x)


class ManufacturingCost:
    '''
        Class that represents a workhorse job.
    '''
    def __init__(self, name, material_name:str, machine_name:str, time:Q_, material_weight:Q_) -> None:
        self.name = name
        self.material = Materials[material_name]
        self.machine = Machines[machine_name]

        electricity_cost_per_time = CostParameters.price_per_kwh / self.machine.enery_consumption
        self.electricity_cost = ProportionalCost("Electricity", cost_per_1=electricity_cost_per_time, x=time)
        self.material_cost = self.material.price_per_weight * material_weight

        self.value = self.electricity_cost + self.material_cost +  self.machine.amortization_cost
