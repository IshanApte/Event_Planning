import pandas as pd
import math

# Load datasets
event_planning_df = pd.read_csv("Cases.csv")
food_item_df = pd.read_csv("Food_db.csv")
instruction_df = pd.read_csv("Instructions.csv")

def calculate_requirements(event_type, food_type, num_people, num_food_items, num_drink_items, additional_items=None):
    # Retrieve event-specific requirements
    event_requirements = event_planning_df[(event_planning_df['EventType'] == event_type) & (event_planning_df['FoodType'] == food_type)].squeeze()
    
    # Get food items for the event
    event_food_items = event_requirements[['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10']].dropna().values
    if len(event_food_items) >= num_food_items:
        # Select the required number of food items
        suggested_food_items = list(event_food_items[:num_food_items])
    else:
        # Select all available food items and calculate the remaining required items
        suggested_food_items = list(event_food_items)
        num_remaining_items = num_food_items - len(event_food_items)
        remaining_items = food_item_df[(food_item_df['Type'] == food_type) & (~food_item_df['Food'].isin(event_food_items))]['Food'].values[:num_remaining_items]
        suggested_food_items.extend(list(remaining_items))
    
    # Get drink items for the event
    event_drink_items = event_requirements[['D1', 'D2', 'D3', 'D4']].dropna().values.flatten()
    
    if len(event_drink_items) >= num_drink_items:
        # Select the required number of drink items
        suggested_drink_items = list(event_drink_items[:num_drink_items])
    else:
        # Select all available drink items and calculate the remaining required items
        suggested_drink_items = list(event_drink_items)
        num_remaining_drink_items = num_drink_items - len(event_drink_items)
        remaining_drink_items = food_item_df[(food_item_df['Type'] == 'Drinks') & (~food_item_df['Food'].isin(event_drink_items))]['Food'].values[:num_remaining_drink_items]
        suggested_drink_items.extend(list(remaining_drink_items))
    
    
    # Combine additional items with suggested items if provided
    if additional_items:
        for item in additional_items:
            item_type = food_item_df[(food_item_df['Food'] == item)]['Type'].values[0]
            if item_type == 'Drinks':
                suggested_drink_items.append(item)
            else:
                suggested_food_items.append(item)
    
    suggested_items = suggested_food_items + suggested_drink_items
    
    # Calculate utensil requirements based on the selected food items
    required_utensils = {}
    for food_item in suggested_items:
        if food_item:
            food_item_info = food_item_df.loc[food_item_df['Food'] == food_item].dropna(axis=1)
            if not food_item_info.empty:
                utensil_names = food_item_info.columns[2:]
                utensil_values = food_item_info.values[0][2:]
                for name, value in zip(utensil_names, utensil_values):
                    if value != 0:
                        required_utensils[name] = required_utensils.get(name, 0) + value

    # Calculate Tables, Plates, BevNaps, Workers, TableClothes, SaltPepper, SignStands, CutleryKits, WireBasket, HotCups, ColdCups, CreamerPitcher, SugarCaddy
    other_items = ['Tables', 'Plates', 'BevNaps', 'TableClothes', 'SaltPepper', 'SignStands', 'CutleryKits', 'WireBasket', 'HotCups', 'ColdCups', 'CreamerPitcher', 'SugarCaddy']
    required_items = dict()
    
    for items in other_items:
        item_value = math.ceil((event_requirements[items]/event_requirements['Guests']) * num_people)
        if item_value > 0:
            required_items[items] = item_value

            
    # Generate instructions
    instructions = instruction_df.drop(columns=['Event']).iloc[0].values  # Assuming all events have the same instructions
    final_instructions = []
    for instruction in instructions:
        if 'Plates,BevNaps,HotCups' in instruction:
            item_list = instruction[13:]
            item_list = item_list.split(',')
            final_items = []
            for item in item_list:
                if item in required_items:
                    final_items.append(item)
            
            new_instruction = instruction[:13] + ','.join(final_items)
            
            final_instructions.append(new_instruction)
        else:
            final_instructions.append(instruction)
    
    return math.ceil((event_requirements['Workers']/event_requirements['Guests']) * num_people), suggested_food_items, suggested_drink_items, pd.Series(required_items), pd.Series(required_utensils), final_instructions

# _,_,_,_,_,ins = calculate_requirements('BoxLunch', 'StandardBoxLunch',15,3,3)
# print(ins)