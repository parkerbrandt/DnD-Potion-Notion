"""
Dungeons & Dragons - Potion Notion

Provides a Dungeon Master the ability to track ingredients and recipes and allow for stochastic gathering of recipes.

Brennen Dahl, Parker Brandt
"""

import csv
import numpy as np
import os
import sys


# Colors for console printing,
W = '\033[0m'   # white (normal)
R = '\033[31m'  # red
O = '\033[33m'  # orange
Y = '\033[93m'  # yellow
G = '\033[32m'  # green


# Global Variables
ingredients_file = "data/ingredients.csv"
inventory_file = "data/inventory.csv"
recipes_file = "data/recipes.csv"

verbosity = 2


"""
Start of Program Logic
"""
if __name__ == "__main__":

    print(f"D&D Potion Notion")

    done = False

    # Load inventory data from CSV file
    # Inventory dict format:
    #   key = String Ingredient Name (i.e. "Rose")
    #   value = Integer Quantity (i.e. 2)
    inventory = {}
    with open(inventory_file, "r") as inv_file:
        invreader = csv.reader(inv_file, delimiter=",")
        for row in invreader:
            inventory[row[0]] = int(row[1])

    while done != True:
        print(f"\nPlease select desired action...")
        t_input = input(f"Actions are:\n\tGather Ingredients (\'gather\'),\n\tView Inventory (\'view\'),\n\tView Recipes (\'view_r\'),\n\tCraft Recipe (\'craft\'),\n\tor Stop (\'stop\')\n\n")
        
        if t_input.lower() == "gather":
            # Gather ingredients
            num_rolls = int(input("How many ingredients?\n"))

        elif t_input.lower() == "view":
            # Display the inventory
            print(f"Displaying current inventory...")

            for ingredient, quantity in inventory.values():
                print(f"\t{quantity} {ingredient}")         # TODO: Could add more info about when/where
        
        elif t_input.lower() == "view_r":
            # Display all recipes
            print(f"Displaying recipes...")

            with open(recipes_file, "r") as rec_file:
                recreader = csv.reader(rec_file, delimiter=",")
                for row in recreader:

                    # Ignore the header row
                    if row[0] != "Recipe Name":
                        output = f"{row[0]} = "

                        ingredients = row[1].split("|")
                        quantities = row[2].split("|")
                        for i, c in enumerate(ingredients):
                            output += f"{quantities[i]} {c}"

                            if i < len(ingredients) - 1:
                                output += " + "
                        
                        # TODO: Check if this ingredient is craftable
                        print(f"\t{output}")
        
        elif t_input.lower() == "craft":
            # Craft a recipe and put into inventory
            print(f"Craft a Recipe...")

        elif t_input.lower() == "stop":
            # Stop the loop and exit
            print(f"Stopping...")
            done = True

        else:
            print(f"Invalid arguments. Please select another option.")