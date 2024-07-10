
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
            "m": 3600,  # Meters to millimeters
        },
        "currency": { # TODO: add more currencies / API to get the conversion rates
            "eur": 1,  # Euro (base unit)
            "huf": 300,  # HUF to Euro
            "gbp": 0.8,  # British Pound to Euro
        }
    }

    def __init__(self, value, unit):
        self.value = value
        self.unit = unit.lower()  # Ensure unit is lowercase for case-insensitive handling

        self.factors = None
        for key, value in Value.conversion_factors.items():
            if self.unit in value and not self.type:
                self.factors = key

        if not self.type:
            raise ValueError(f"Given {unit=} not supported")

    def to(self, target_unit):
        """Converts the value to the specified target unit.

        Raises:
            ValueError: If the target unit is not supported.
        """

        if self.unit not in conversion_factors or target_unit not in conversion_factors[self.unit]:
            raise ValueError(f"Conversion from {self.unit} to {target_unit} not supported")

        # Perform unit conversion
        conversion_factor = conversion_factors[self.unit][target_unit]
        self.value *= conversion_factor
        self.unit = target_unit

    def __str__(self):
        """Provides a user-friendly string representation of the measurement."""
        return f"{self.value:.2f} {self.unit}"
