import re

class House:
    def __init__(self, price, address, specs):
        self.price = price
        self.address = address
        self.specs = specs

    def get_spec(self, spec):
        try:
            value = self.specs[spec].replace("\n", " ")
            if spec=="basement" and value!="No":
                return "yes"
            if spec == "living area" or spec == "surface of the plot" or spec == "kitchen surface":
                return value.split("m²")[0].strip()
            if spec == "primary energy consumption":
                return value.split("kwh/m²")[0].strip()
            if spec == "street frontage width":
                return int(re.sub("[^0-9]", "", value))
            return value.strip()
        except KeyError:
            return None

    def get_price(self):
        return int(re.sub("[^0-9]", "", self.price))
