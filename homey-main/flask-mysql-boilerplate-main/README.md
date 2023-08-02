# MySQL + Flask Boilerplate Project

# Project name: Homey

# 1. Description of database
Introducing Homey, the ultimate solution for managing shared living spaces with ease and grace. Our web-based application is designed to keep you and your roommates, housemates, or family in perfect harmony. Say goodbye to arguments about whose turn it is to clean the bathroom or pay the bills, and hello to a beautifully organized and connected household! With Homey, you can streamline your chores with our to-do list that comes with automated reminders, and a synced calendar that displays scheduled chores, outings, and other tasks or events. Plus, our shared shopping list makes it easy to manage purchases as a group. Our messaging platform is integrated with all of Homey's services, making it easy to communicate with your roommates, housemates, or family.

# 2. Set up
This repo contains a boilerplate setup for spinning up 3 Docker containers: 
- A MySQL 8 container used to manage and manipulate data in the database
- A Python Flask container to implement a REST API
- A Local AppSmith Server

## How to setup and start the containers
**Important** - you need Docker Desktop installed
- Clone this repository.  
- Create a file named `db_root_password.txt` in the `secrets/` folder and put inside of it the root password for MySQL. 
- Create a file named `db_password.txt` in the `secrets/` folder and put inside of it the password you want to use for the a non-root user named webapp. 
- In a terminal or command prompt, navigate to the folder with the `docker-compose.yml` file.  
- Build the images with `docker compose build`
- Start the containers with `docker compose up`.  To run in detached mode, run `docker compose up -d`. 

# 3. Data Schema
- users: Information about household members using the app
- tasks: Task details, including date, time, assignee, and assignor
- messages: Message exchanges between household members using the app
- shopping_items: Shopping items required by household members
- shopping_categories: Shopping categories used by household members
- tasks_categories: Task categories
- events: Event information for household members using the app
- event_attendees: Information about household members attending events

# 4. Usage
To use the database, follow these steps:

- Launch the application by running the app.py file with Python 3.
- Open a web browser and navigate to the URL http://localhost:8001.
- Access all features on the homepage.


# 5. Link to team video : 

https://youtu.be/Vw4xdIBRVog


