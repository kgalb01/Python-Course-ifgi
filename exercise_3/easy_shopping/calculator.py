# Python in QGIS and ArcGIS
# Exercise 3
# Author: Jonas Starke, Kieran Galbraith
# Date: 2024-23-04

class Calculator:
    def add(self, x, y):
        return x + y

    def subtract(self, x, y):
        return x - y

    def multiply(self, x, y):
        return x * y

    def divide(self, x, y):
        if y == 0:
            raise ValueError("Cannot divide by zero")
        return x / y