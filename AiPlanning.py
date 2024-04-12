import sqlite3

def setup_database():
    conn = sqlite3.connect('event_planning.db')
    cursor = conn.cursor()
    # Create or open the database and setup tables for food and utensils requirements
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS food_requirements (
        event_type TEXT,
        item TEXT,
        quantity_per_person REAL
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS utensil_requirements (
        event_type TEXT,
        item TEXT,
        utensil TEXT,
        quantity_per_item REAL
    )
    ''')
    conn.commit()
    conn.close()

def insert_food_requirement(event_type, item, quantity_per_person):
    conn = sqlite3.connect('event_planning.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO food_requirements (event_type, item, quantity_per_person) VALUES (?, ?, ?)',
                   (event_type, item, quantity_per_person))
    conn.commit()
    conn.close()

def insert_utensil_requirement(event_type, item, utensil, quantity_per_item):
    conn = sqlite3.connect('event_planning.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO utensil_requirements (event_type, item, utensil, quantity_per_item) VALUES (?, ?, ?, ?)',
                   (event_type, item, utensil, quantity_per_item))
    conn.commit()
    conn.close()

def fetch_utensils(event_type, items):
    conn = sqlite3.connect('event_planning.db')
    cursor = conn.cursor()
    utensils = {}
    for item in items:
        cursor.execute('SELECT utensil, quantity_per_item FROM utensil_requirements WHERE event_type = ? AND item = ?', (event_type, item))
        fetched_utensils = cursor.fetchall()
        utensils[item] = {utensil: quantity for utensil, quantity in fetched_utensils}
    conn.close()
    return utensils

class Event:
    def __init__(self, event_type, number_of_people):
        self.event_type = event_type
        self.number_of_people = number_of_people

    def fetch_requirements(self):
        food_items = fetch_food_items(self.event_type, self.number_of_people)
        utensils_needed = fetch_utensils(self.event_type, list(food_items.keys()))
        return food_items, utensils_needed

    def additional_requirements(self):
        # This method can be overridden by subclasses if additional requirements are needed
        pass
    
def fetch_food_items(event_type, number_of_people):
    conn = sqlite3.connect('event_planning.db')
    cursor = conn.cursor()
    # Retrieve the required food items for the given event type
    cursor.execute('SELECT item, quantity_per_person FROM food_requirements WHERE event_type = ?', (event_type,))
    items = cursor.fetchall()
    conn.close()

    # Calculate the total amount of each item needed based on the number of people
    requirements = {item: quantity * number_of_people for item, quantity in items}
    return requirements

class BoxLunch(Event):
    def additional_requirements(self):
        # Box lunch might require additional items like disposable cutlery
        return {"disposable cutlery": self.number_of_people}

class Buffet(Event):
    def additional_requirements(self):
        # Buffet might require additional items like chafing dishes for food serving
        return {"chafing dishes": max(1, self.number_of_people // 50)}  # One per 50 attendees

class ServeDinner(Event):
    def additional_requirements(self):
        # Served dinners might require a higher standard of utensils and additional decorations
        return {"table decorations": max(1, self.number_of_people // 10)}  # One decoration per table of 10


def setup_examples():
    # Create examples of each type of event
    box_lunch_event = BoxLunch("BoxLunch", 100)
    buffet_event = Buffet("Buffet", 150)
    dinner_event = ServeDinner("ServeDinner", 80)

    # Fetch and print the basic and additional requirements for each event
    print("Box Lunch Event:")
    print(box_lunch_event.fetch_requirements())
    print(box_lunch_event.additional_requirements())

    print("\nBuffet Event:")
    print(buffet_event.fetch_requirements())
    print(buffet_event.additional_requirements())

    print("\nServe Dinner Event:")
    print(dinner_event.fetch_requirements())
    print(dinner_event.additional_requirements())

setup_examples()
# Setup the database (run this once)
# setup_database()

# Example of how to use the Event class
event = BoxLunch("BoxLunch", 100)  # For 100 people
food_requirements, utensils = event.fetch_requirements()
print("Food Requirements:", food_requirements)
print("Utensils Needed:", utensils)