
class Value:
    conversion_factors = {
        "time": {
            "s": 1,  # Seconds (base unit)
            "min": 60,  # Minutes to seconds
            "h": 3600,  # Hours to seconds
            "day" : 86400, # Days to seconds
        },
        "distance": {
            "mm": 1,  # Millimeters (base unit)
            "cm": 10,  # Centimeters to millimeters
            "m": 1000,  # Meters to millimeters
        },
        "energy": {
            "wmin": 1,
            "wh": 60,
            "kwmin": 1000,
            "kwh": 60000,
        },
        "unitless": { # default
            "-": 1,
        },
        "currency": { # TODO: add more currencies / API to get the conversion rates
            "huf": 1,  # HUF to Euro
            "eur": 300,  # Euro (base unit)
            "gbp": 400,  # British Pound to Euro
        }
    }

    def __init__(self, value, unit = "-"):
        self.value = value
        self.unit = unit
        self._unit = unit.lower()  # Ensure unit is lowercase for case-insensitive handling

        self.factor = None
        for k, v in Value.conversion_factors.items():
            if self.unit in v and not self.factor:
                self.factor = Value.conversion_factors[k]

        if not self.factor:
            raise ValueError(f"Given {unit=} not supported")

    def to(self, target_unit:str):
        """Converts the value to the specified target unit.

        Raises:
            ValueError: If the target unit is not supported.
        """

        if target_unit not in self.factor :
            raise ValueError(f"Conversion from {self.unit} to {target_unit} not supported")

        # Perform unit conversion
        self.value *= (self.factor[self.unit] / self.factor[target_unit.lower()])
        self.unit = target_unit

    def get(self):
        return self.value

    def __str__(self):
        """Provides a user-friendly string representation of the value."""
        return f"{self.value:.4f} {self.unit}"

if __name__ == "__main__":
    val = Value(1, "kwh")
    val.to("wh")
    print(val)