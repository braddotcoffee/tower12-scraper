class Apartment:
    def __init__(
        self,
        unit: str = "",
        floor: int = 0,
        floorplan: str = "",
        price: str = "",
        availability: str = "",
    ):
        self.unit = unit
        self.floor = floor
        self.floorplan = floorplan
        self.price = price
        self.availability = availability

    def __repr__(self):
        return (
            f"Apartment {self.unit}\n"
            + "---------\n"
            + f"Floor: {self.floor}\n"
            + f"Floorplan: {self.floorplan}\n"
            + f"Price: {self.price}\n"
            + f"Availability: {self.availability}\n"
        )

    def __hash__(self):
        return hash((self.unit, self.floor, self.floorplan, self.price))

    def __eq__(self, other):
        return (
            self.unit == other.unit
            and self.floor == other.floor
            and self.floorplan == other.floorplan
            and self.price == other.price
        )

    def to_message(self) -> str:
        msg = "```\n"
        msg += str(self)
        msg += "```\n"
        return msg
