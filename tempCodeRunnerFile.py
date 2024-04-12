# Setup the database (run this once)
setup_database()

# Example of how to use the Event class
event = BoxLunch("BoxLunch", 100)  # For 100 people
food_requirements, utensils = event.fetch_requirements()
print("Food Requirements:", food_requirements)
print("Utensils Needed:", utensils)