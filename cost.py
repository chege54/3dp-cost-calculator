
class Printer:
    '''
        Printer is a class that represents a 3D printer.
    '''
    def __init__(self, name, enery_consumption, price = 0, amortization_hour = 0, service_cost = 0) -> None:
        self.name = name
        self.enery_consumption = enery_consumption
        self.price = price
        self.amortization_hour = amortization_hour
        self.service_cost = service_cost

    @property
    def amortization_per_hour(self):
        total_cost = (self.price + self.service_cost)

        if total_cost > 0 and self.amortization_hour > 0:
            result = total_cost / self.amortization_hour
        else:
            result = 0

        return result


class Material:
    '''
        Material is a class that represents a 3D printing material.
    '''
    def __init__(self, name, price, diameter_mm, spool_g, density_g_cm3 = 0, length_mm = 0) -> None:
        self.name = name

        if length_mm > 0:
            self.length = length_mm

        if density_g_cm3 > 0:
            self.density = density_g_cm3
            # l = weight / (density * cross_section_area_cm2)
            cross_section_area_cm2 = (diameter_mm * diameter_mm/100) * 3.1415 / 4 # area is in cm2
            calculated_length = (spool_g / (density_g_cm3 * cross_section_area_cm2)) * 10 # convert to mm
            print(f"{calculated_length=}" ) #TODO: add logging
            self.length = calculated_length

        self.price_per_g = price / spool_g
        self.price_per_mm = price / self.length

class CostParameters: # TODO: move to config file
    currency = "EUR"
    enery_cost_per_hour = 0.3 # in EUR per kWh
    manual_cost_per_hour = 30 # in EUR per kWh
    safety_factor = 5 # in percent

class OneTimeCost:
    '''
        Cost is a class that represents the one time costs.
    '''
    def __init__(self, name, cost) -> None:
        self.name = name
        self.cost = cost


class ProportionalCost:
    '''
        Cost is a class that represents the proportional costs.
    '''
    def __init__(self, name, cost_per_1, x) -> None:
        self.name = name
        self.cost_per_x = cost_per_1
        self.value = cost_per_1 * x


ManualJobs = {
    "project": {
        "cleaning": ProportionalCost("Cleaning", time_min = 5),
        "calibration": ProportionalCost("Calibration", time_min = 5),
        "material_change": ProportionalCost("Material change", time_min = 5),
        "other": ProportionalCost("Other", time_min = 1),
    },
    "print": {
        "modelling": Cost("Modelling", time_min = 30),
        "slicing": Cost("Slicing", time_min = 10),
        "start_remove_print": Cost("Start/Remove Print", time_min = 1),
        "post_processing": Cost("Post processing/Remove support", time_min = 1),
        "other": Cost("Other", time_min = 1),
    }
}


class PreparationTime:
    '''
        Preparation is a class that represents a 3D print preparation.
    '''
    def __init__(self, name, time, cost = 0) -> None:
        self.name = name
        self.time = time
        self.cost = cost

class PrintJob:
    '''
        Job is a class that represents a 3D print job.
    '''
    def __init__(self) -> None:
        pass

if __name__ == "__main__":
    pass