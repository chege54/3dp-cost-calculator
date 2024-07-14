from pint_units import Q_, ureg
from parameters import CostParameters

class Machine:
    '''
        Machine is a class that represents a 3D printer or any similar workhorse.
    '''
    def __init__(self, name:str,
                 enery_consumption:Q_,
                 machine_price:Q_,
                 amortization_time:Q_,
                 service_cost:Q_) -> None:
        self.name = name
        self.enery_consumption = enery_consumption
        self.machine_price = machine_price
        self.amortization_time = amortization_time
        self.service_cost = service_cost

    def get_amortization_cost(self, time:Q_) -> Q_:
        total_cost = (self.machine_price + self.service_cost)

        if total_cost > 0 and self.amortization_time > 0:
            result = total_cost / self.amortization_time
        else:
            result = 0

        return (result * time).to_base_units()

    def get_electricity_cost(self, time:Q_) -> Q_:
        electricity_cost = ((CostParameters.price_per_kwh * self.enery_consumption) * time).to_base_units()
        return electricity_cost


#### Machine database ####
Machines = {
    "SnapmakerA350" : Machine(name="Snapmaker A350",
                              enery_consumption= 300 * ureg.watt,
                              machine_price=     640000 * ureg.dimensionless,
                              amortization_time= 5000 * ureg.hour,
                              service_cost=      30000 * ureg.dimensionless)
}
