# Python in QGIS and ArcGIS
# Exercise 3
# Author: Jonas Starke, Kieran Galbraith
# Date: 2024-25-04

class ShoppingCart:
    def __init__(self):
        self.items = {}

    def add_item(self, item, quantity):
        if item in self.items:
            self.items[item] += quantity
        else:
            self.items[item] = quantity

    def remove_item(self, item):
        if item in self.items:
            del self.items[item]
        else:
            print(f"{item} not found in the cart.")

    def total_quantity(self):
        return sum(self.items.values())