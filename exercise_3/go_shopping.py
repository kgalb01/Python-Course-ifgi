# Python in QGIS and ArcGIS
# Exercise 3
# Author: Jonas Starke, Kieran Galbraith
# Date: 2024-25-04

from easy_shopping.calculator import Calculator
from easy_shopping.shopping import ShoppingCart

def main():
    # Create a new calculator
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


    # Create a new shopping cart
    cart = ShoppingCart()

    # Add items to the cart
    cart.add_item("Apple", 3)
    cart.add_item("USB Stick", 2)
    cart.add_item("Beer", 25)

    # Display current items and total quantity
    print("Current items in the cart:")
    for item, quantity in cart.items.items():
        print(f"{item}: {quantity}")

    print("Total quantity in the cart:", cart.total_quantity())

    # Remove an item from the cart
    cart.remove_item("Beer")

    # Display updated items and total quantity
    print("Updated items in the cart:")
    for item, quantity in cart.items.items():
        print(f"{item}: {quantity}")

    print("Total quantity in the cart:", cart.total_quantity())

    # Remove an non-existent item from the cart
    cart.remove_item("Banana")

    # Display updated items and total quantity
    print("Updated items in the cart:")
    for item, quantity in cart.items.items():
        print(f"{item}: {quantity}")

    print("Total quantity in the cart:", cart.total_quantity())

if __name__ == "__main__":
    main()