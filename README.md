# Event Planning Application

## Description

The Event Planning Application is a tool that helps users plan various types of events by providing suggestions for food and drink items, calculating the required number of workers, and listing necessary items and utensils. The application allows users to input details such as event type, food type, number of people attending, and additional food or drink items to be included (optional).

## Features

- Calculate the number of workers required based on the number of guests.
- Provide suggested food and drink items for the event.
- List required items such as tables, plates, etc.
- List required utensils required for serving the food and drinks.
- Display instructions for organizing the event.

## Installation

1. Clone the repository to your local machine.
2. Install the required dependencies by running `pip install -r requirements.txt`.
3. Ensure that the CSV files (`Cases.csv`, `Food_db.csv`, `Instructions.csv`) are present in the project directory.

## Usage

1. Run the `ui.py` file using Python.
2. Enter the details of your event
   1. Event type
   2. Food type
   3. Number of Guests
   4. Number of Food items
   5. Number of Drink items
   6. Additional Food or Drink items (optional)
3. Click the "Calculate" button to generate event planning suggestions.
4. View the number of workers required, suggested food items, suggest drink items, required items for setting up the event, required utensils, and instructions displayed in the application window.

## CSV Files

- **Cases.csv**: Contains event-specific requirements such as even type, food type, food items in the event, drink items in the event, number of guests, workers, and other items.
- **Food_db.csv**: Provides information about food and drink items, including their types and associated utensils.
- **Instructions.csv**: Contains general instructions for organizing events.

## Contributing

Contributions are welcome! If you'd like to contribute to the project, feel free to fork the repository and submit a pull request.
