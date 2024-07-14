from pint_units import ureg

class CostParameters: # TODO: move to config file
    currency = "huf" # TODO: currently it is "dimensionless"
    price_per_kwh        = 40 * ureg.dimensionless / (ureg.kilowatt*ureg.hour)  # in price per kWh
    manual_cost_per_hour = 10000 * ureg.dimensionless / ureg.hour # in huf per hour
    safety_factor        = 5 * ureg.percent # in percent