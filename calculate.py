from cost import ManualCost, FixCost, ManufacturingCost
from pint_units import Q_, ureg

Jobs = {
    "per_project": {
        "cleaning":         ManualCost("Cleaning",          x = 2 * ureg.minutes),
        "calibration":      ManualCost("Calibration",       x = 5 * ureg.minutes),
        "material_change":  ManualCost("Material change",   x = 5 * ureg.minutes),
        "other_1":          FixCost("Alcohol",              x = 300 * ureg.dimensionless),
    },
    "per_print": {
        "modelling":          ManualCost("Modelling",                       x = 15* ureg.minutes),
        "slicing":            ManualCost("Slicing",                         x = 10* ureg.minutes),
        "start_remove_print": ManualCost("Start/Remove Print",              x = 10* ureg.minutes),
        "post_processing":    ManualCost("Post processing/Remove support",  x = 10* ureg.minutes),
        "other":              ManualCost("Other",                           x = 10* ureg.minutes),
    }
}

if __name__ == "__main__":
    pass

