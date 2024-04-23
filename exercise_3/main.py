# Python in QGIS and ArcGIS
# Exercise 3
# Author: Jonas Starke, Kieran Galbraith
# Date: 2024-23-04

from calculator import Calculator

def main():
    calc = Calculator()
    
    try:
        result1 = calc.add(7, 5)
        print("Result of 7 + 5 =", result1)

        result2 = calc.subtract(34, 21)
        print("Result of 34 - 21 =", result2)

        result3 = calc.multiply(54, 2)
        print("Result of 54 * 2 =", result3)

        result4 = calc.divide(144, 2)
        print("Result of 144 / 2 =", result4)

        result5 = calc.divide(45, 0)
        print("Result of 45 / 0 =", result5)

    except ValueError as e:
        print("Error:", e)

if __name__ == "__main__":
    main()