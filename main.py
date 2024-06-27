"""
Dungeons & Dragons - Potion Notion

Provides a Dungeon Master the ability to stochastically 

Brennen Dahl, Parker Brandt
"""

import csv
import numpy as np
import os
import sys


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

    while done != True:
        print(f"\nPlease select desired action...")
        t_input = input(f"Actions are:\n\tGather Ingredients (\'gather\'),\n\tView Inventory (\'view\'),\n\tView Recipes (\'view_r\'),\n\tCraft Recipe (\'craft\'),\n\tor Stop (\'stop\')\n\n")
        
        if t_input.lower() == "gather":
            # Gather ingredients
            num_rolls = int(input("How many ingredients?"))

        elif t_input.lower() == "view":
            # Display the inventory
            print(f"Displaying current inventory...")

            with open(inventory_file, "w") as inv_file:
                invreader = csv.reader(inv_file, delimiter=",")
                for row in invreader:
                    print()
        
        elif t_input.lower() == "view_r":
            # Display all recipes
            print(f"Displaying recipes...")
        
        elif t_input.lower() == "craft":
            # Craft a recipe and put into inventory
            print(f"Craft a Recipe...")

        elif t_input.lower() == "stop":
            # Stop the loop and exit
            print(f"Stopping...")
            done = True

        else:
            print(f"Invalid arguments. Please select another option.")