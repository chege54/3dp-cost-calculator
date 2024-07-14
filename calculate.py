from cost import ManualCost, FixCost, ManufacturingCost
from pint_units import Q_, ureg
import pandas as pd
import numpy as np
import glob
from pathlib import Path
import re

# One time project specific costs
PER_PROJECT_COSTS = [
    ManualCost("Cleaning",              x = 2 * ureg.minutes),
    ManualCost("Calibration/Leveling",  x = 10 * ureg.minutes),
    ManualCost("Material change",       x = 5 * ureg.minutes),
    FixCost("Alcohol",                  x = 500 * ureg.dimensionless),
    FixCost("Glue",                     x = 4250 * ureg.dimensionless),
]

# This costs are not multiplied - but post processing could be piecewise...
per_print_costs = [
    ManualCost("Modelling",                       x = 30 * ureg.minutes),
    ManualCost("Slicing",                         x = 15 * ureg.minutes),
    ManualCost("Start/Remove print",              x = 5 * ureg.minutes),
    ManualCost("Post processing/Remove support",  x = 5 * ureg.minutes),
]


if __name__ == "__main__":
    # Convert costs to pandas df for simpler excel export
    per_project_df = pd.DataFrame((cost.name, str(cost.get_cost())) for cost in PER_PROJECT_COSTS).T
    series_pd = list()

    #collect all gcode files
    target_folder = Path("./gcode")
    gcode_files = glob.glob(f"{target_folder}/**/*.gcode", recursive=True)

    for gcode_file in gcode_files:
        gcode_file_path = Path(gcode_file)
        # parse multipliers from from folder names like: 'print-job_5x' which means print 5 times
        match = re.match("\S+_(\d+)+x$", gcode_file_path.parent.name, re.IGNORECASE)
        multiplier = int(match.group(1)) if match else 1
        # parse gcode meta data from its header section. TODO: currently Snapmaker luban supported
        # TODO parse material type and pass it to the ManufacturingCost calc. object
        with gcode_file_path.open() as f:
            for line in f:
                if line.startswith(";estimated_time"):
                    estimated_time = re.match("^;estimated_time\(s\):\s+((\d+\.?\d*))",line).group(1)
                    estimated_time = float(estimated_time) * ureg.second
                if line.startswith(";matierial_weight"):
                    material_weight = re.match("^;matierial_weight:\s+((\d+\.?\d*))",line).group(1)
                    material_weight = float(material_weight) * ureg.gram
                if line.startswith(";matierial_length"):
                    material_length = re.match("^;matierial_length:\s+((\d+\.?\d*))",line).group(1)
                    material_length = float(material_length) * ureg.meter
                if line.startswith(("G,M,T")):
                    # Valid gcode found, stop further parsing
                    break
        # Manufacturing cost
        manufacturing_cost = ManufacturingCost(name = gcode_file, machine_name="SnapmakerA350", material_name="PLA", material_weight=material_weight, time=estimated_time)

        # Helpers to collect detailed values
        manuf_cost_details = manufacturing_cost.get_details()
        per_print_details = [(cost.name, str(cost.get_cost())) for cost in per_print_costs]

        manual_cost_per_file = np.sum([cost.get_cost() for cost in per_print_costs])
        final_price_per_print = manufacturing_cost.get_cost() * multiplier + manual_cost_per_file # Modelling, slicing etc.. are not multiplied
        # All information per print
        details = [ ("File",gcode_file),
                    *manuf_cost_details,
                    *per_print_details,
                    ("printing cost", str(manufacturing_cost.get_cost())),
                    ("manual cost", str(manual_cost_per_file)),
                    ("piece(s)", multiplier),
                    ("total", str(final_price_per_print))]

        idx, values = zip(*details)
        series_pd.append(pd.Series(values, index=idx))

    per_print_df = pd.DataFrame(series_pd)

    with pd.ExcelWriter('output.xlsx') as writer:
        per_print_df.to_excel(writer, sheet_name='print_costs')
        per_project_df.to_excel(writer, sheet_name='project_costs')

