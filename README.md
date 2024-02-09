# Data Tracker

## Description
Data Tracker is a Python-based tkinter application designed to run silently in the background of your computer. It starts automatically upon system startup and collects daily user responses through dialog boxes based on pre-configured yes/no questions. These responses are stored in a SQLite database for future analysis. The application also features a settings menu accessible through a desktop icon, allowing users to configure questions and view the last collection date. This menu also provides an option to manually collect data at any time.

## Features
- Runs on system startup, operating silently in the background.
- Collects daily user responses through simple dialog boxes.
- Configurable questions stored in a SQLite database.
- Settings menu for question configuration and manual data collection.
- Future plans include a React app for data visualization.

## Installation
(Currently in development. Detailed steps for setup and configuration will be provided upon completion of packaging with PyInstaller.)

## Initial Setup
1. Clone the repository to your local system.
2. Ensure Python is installed on your computer.
3. (Placeholder for PyInstaller packaging instructions.)

## Configuring Questions
- Access the settings menu via the desktop icon.
- View, add, or modify questions through the settings interface.
- New questions require specifying the question text, column name for storage, and question type (currently limited to yes/no).

## Collecting Data
- The app automatically prompts for daily data collection based on system startup and user activity.
- Manual data collection can be initiated through the settings menu.

## Architecture
Data Tracker is built following the Model-View-Controller (MVC) architectural pattern, ensuring a clear separation of concerns within the application:
- **Model:** Manages the database connections, queries, and table manipulations. It is responsible for handling all data logic and interactions with the SQLite database, including checking, reading, and writing to the database tables.
- **View:** Comprises several tkinter interfaces, including the settings page, homepage, and data collector. The view layer is responsible for presenting data to the user and capturing user inputs.
- **Controller:** Acts as an intermediary between the Model and View. It manages user interactions with the tkinter views, processing inputs, and directing data flow to and from the Model.

This structured approach not only facilitates easier maintenance and scalability of the application but also demonstrates a solid understanding of MVC, a valuable skill in software development.

## Future Enhancements
- Addition of new question types (text input, numeric input).
- Development of a React-based dashboard for enhanced data visualization.

**Note:** This README includes placeholders for future development steps and features that are currently in the planning stage. Users are encouraged to check back for updates.
