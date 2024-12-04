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
auto_roll = False


"""
Start of Program Logic
"""
if __name__ == "__main__":

    print(f"D&D Potion Notion")

    done = False

    # Load recipe data from CSV file
    # Recipe dict format:
    #   key = String Recipe Name (i.e. "Healing Potion")
    #   value = Dict of Ingredient Names and Quantities (i.e. {"Rose": 1, "Water": 2})
    recipes = {}
    with open(recipes_file, "r") as rec_file:
        recreader = csv.reader(rec_file, delimiter=",")
        for row in recreader:
            if row[0] != "Recipe Name":
                
                # Separate all ingredients and quantities
                ing_dict = {}
                ingredients = row[1].split("|")
                quantities = row[2].split("|")
                
                for i, c in enumerate(ingredients):
                    ing_dict[c] = int(quantities[i])

                recipes[row[0]] = ing_dict

    # Load inventory data from CSV file
    # Inventory dict format:
    #   key = String Ingredient Name (i.e. "Rose")
    #   value = Integer Quantity (i.e. 2)
    inventory = {}
    with open(inventory_file, "r") as inv_file:
        invreader = csv.reader(inv_file, delimiter=",")
        for row in invreader:
            if row[0] != "Ingredient Name":
                inventory[row[0]] = int(row[1])

    while done != True:
        print(f"\nPlease select desired action...")
        t_input = input(f"Actions are:\n\tGather Ingredients (\'gather\'),\n\tView Inventory (\'view\'),\n\tView Recipes (\'view_r\'),\n\tCraft Recipe (\'craft\'),\n\tor Stop (\'stop\')\n\n")
        
        if t_input.lower() == "gather":
            # Gather ingredients

            environ = input("What is the current environment?\n")

            # Get all legal ingredients for this environment
            legal_ingredients = {}
            with open(ingredients_file, 'r') as ingfile:
                ingreader = csv.reader(ingfile, delimiter=',')
                for row in ingreader:
                    if row[0] != "Ingredient Name":
                        possible_envs = row[1].split('|')
                        rarities = row[2].split('|')

                        if environ in possible_envs:
                            legal_ingredients[row[0]] = float(rarities[possible_envs.index(environ)])

                            # TODO: Print legal ingredients


            die_result = 0
            if auto_roll:
                # Roll a die
                die_result = np.random.uniform(1, 20)
                print(f"{Y}You have rolled a {die_result}{W}")
            else:
                die_result = int(input(f"Roll a D20: "))

            # Use die_result to gen a float between 0 and 1 
            percents = []
            for i in range(die_result):
                percents.append(np.random.uniform(0, 1))

            # Choose the ingredient with the rarity closest to the smallest
            smallest_chance = min(percents)
            rarest_ingredient = ""
            smallest_diff = 100
            for ingredient, rarity in legal_ingredients.items():
                test_diff = abs(smallest_chance - rarity)
                if test_diff < smallest_diff:
                    rarest_ingredient = ingredient
                    smallest_diff = test_diff

            # Add that item to the inventory
            if rarest_ingredient in inventory.keys():
                inventory[rarest_ingredient] = inventory.get(rarest_ingredient) + 1
            else:
                inventory[rarest_ingredient] = 1


        elif t_input.lower() == "view":
            # Display the inventory
            print(f"Displaying current inventory...")

            for ingredient, quantity in inventory.items():
                print(f"\t{quantity} {ingredient}")
        
        elif t_input.lower() == "view_r":
            # Display all recipes
            print(f"Displaying recipes...")

            for recipe, ingredients in recipes.items():
                output = f"{recipe} = "

                craftable = True
                for ingredient, quantity in ingredients.items():
                    output += f"{quantity} {ingredient} + " # TODO: Remove last +

                    # Check if there are enough ingredients in the inventory
                    if ingredient not in inventory.keys():
                        craftable = False
                    else:
                        # We have the ingredient, just need to check the quantity
                        num_owned = inventory.get(ingredient)
                        if num_owned < quantity:
                            craftable = False

                # Output and use colors to show if it is craftable or not
                if craftable:
                    print(f"{G}", end="")
                else:
                    print(f"{R}", end="")
                print(f"\t{output}{W}")                        
        
        elif t_input.lower() == "craft":
            # Craft a recipe and put into inventory
            # Get the recipe to craft
            craft_rec = input(f"Which recipe to craft?\n")

            try:
                ingredients = recipes[craft_rec]

                # Check that all ingredients/quantities are available
                craftable = True
                for ingredient, quantity in ingredients.items():
                    if ingredient not in inventory.keys():
                        craftable = False
                    else:
                        num_owned = inventory.get(ingredient)
                        if num_owned < quantity:
                            craftable = False

                if craftable:
                    # Remove all necessary ingredients from inventory
                    for ingredient, quantity in ingredients.items():
                        inventory[ingredient] = inventory.get(ingredient) - quantity
                        if inventory.get(ingredient) == 0:
                            # Remove the ingredient from the inventory
                            del inventory[ingredient]

                    # Add one of the crafted item to the inventory
                    if craft_rec not in inventory.keys():
                        inventory[craft_rec] = 1
                    else:
                        inventory[craft_rec] = inventory.get(craft_rec) + 1

                    # TODO: Overwrite the inventory CSV file with new information
                    with open(inventory_file, 'w') as invfile:
                        writer = invfile.writer()
                else:
                    print(f"{R}Could not craft: Missing ingredients{W}")
                
            except:
                print(f"Invalid Recipe, try again")

        elif t_input.lower() == "stop":
            # Stop the loop and exit
            print(f"Stopping...")
            done = True

        else:
            print(f"Invalid arguments. Please select another option.")