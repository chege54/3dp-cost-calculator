from pint_units import ureg

class CostParameters: # TODO: move to config file
    currency = "huf" # TODO: currently it is "dimensionless"
    price_per_kwh        = 50 * (ureg.dimensionless / ureg.kilowatthour) # in price per kWh
    manual_cost_per_hour = 8400 * (ureg.dimensionless / ureg.hour) # in huf per hour
    safety_factor        = 5 * ureg.percent # in percent