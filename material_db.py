from pint_units import Q_, ureg

class Material:
    '''
        Material is a class that represents a material.
    '''
    def __init__(self, name,
                 price:Q_,
                 diameter:Q_,
                 total_weight:Q_,
                 density:Q_ = None,
                 length:Q_ = None) -> None:
        self.name = name
        self.length = length

        if density:
            self.density = density
            # l = weight / (density * cross_section_area_cm2)
            cross_section_area = (diameter * diameter) * 3.1415 / 4 # area
            calculated_length = (total_weight / (density * cross_section_area)) # convert to mm
            print(f"{calculated_length=}" ) #TODO: add logging
            self.length = calculated_length

        self.price_per_weight = price / total_weight
        self.price_per_length = price / self.length if self.length else None

    def get_cost(self, weight:Q_) -> Q_:
        material_cost = (self.price_per_weight * weight).to_base_units()
        return material_cost

#### Material database ####
Materials = {
    "PLA" : Material(name="3DJAKE ecoPLA",
                     price =        8650 * ureg.dimensionless,
                     diameter =     1.75 * ureg.millimeter,
                     total_weight = 1 * ureg.kilogram)
}