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
        self.cost = x

    def get_cost(self) -> Q_:
        return self.cost


class ProportionalCost:
    '''
        Cost is a class that represents the proportional costs.
    '''
    def __init__(self, name, cost_per_1:Q_, x:Q_) -> None:
        self.name = name
        self.cost_per_x = cost_per_1
        self.cost = (cost_per_1 * x).to_base_units()

    def get_cost(self) -> Q_:
        return self.cost

class ManualCost(ProportionalCost):
    '''
    Handmade costs
    '''
    def __init__(self, name: Q_, x: Q_) -> None:
        super().__init__(name=name, cost_per_1=CostParameters.manual_cost_per_hour, x=x)


class ManufacturingCost:
    '''
        Class that represents a workhorse job.
    '''
    def __init__(self, name, machine_name:str, material_name:str, material_weight:Q_, time:Q_, ) -> None:
        self.name = name
        self.machine = Machines[machine_name]
        self.material = Materials[material_name]
        self.time = time
        self.material_weight = material_weight

        # used for debugging
        self.electricity_cost = self.machine.get_electricity_cost(self.time)
        self.material_cost = self.material.get_cost(self.material_weight)
        self.amortization_cost = self.machine.get_amortization_cost(self.time)

    def get_cost(self):
        total = self.electricity_cost + \
            self.material_cost + \
            self.amortization_cost
        return total

    def get_details(self) -> list:
        return [
            ("Machine", self.machine.name),
            ("Material", self.material.name),
            ("Material weight", str(self.material_weight)),
            ("Material cost", str(self.material_cost)),
            ("Machine time", str(self.time.to('minutes'))),
            ("Electricity cost",str(self.electricity_cost)),
            ("Amortization cost",str(self.amortization_cost)),
        ]
