# final-maxy-bot
Volunteer Task Manager
A streamlined Discord bot for managing volunteer tasks during hackathons and events. Built with Python, discord.py, and SQLite for persistent, high-performance task tracking.

Features
Task Management: Add, claim, complete, and unclaim tasks with simple slash commands.

Live Task Board: A dynamic embed (/tasks) provides a real-time overview of all tasks, categorized by status.

Role-Based Permissions: Command access can be restricted to specific roles (e.g., "Organizer").

Persistent Storage: Task data is stored in an SQLite database, ensuring no data loss on bot restarts.

Optimized for Events: Designed for fast-paced environments where clear task delegation is critical.

🚀 Setup & Deployment
Prerequisites
Python 3.8+

A Discord Application with a Bot Token.

Privileged Gateway Intents (Server Members & Message Content) enabled for the bot.

Installation
Clone the repository:

git clone https://github.com/your-username/Volunteer-Task-Manager.git
cd Volunteer-Task-Manager

Set up a virtual environment:

python -m venv venv
source venv/bin/activate
# On Windows: .\venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Configure environment variables:
Create a .env file in the root directory and populate it with your bot's credentials.

DISCORD_TOKEN=YOUR_BOT_TOKEN_HERE
GUILD_ID=YOUR_SERVER_ID_HERE

Running the Bot
Execute the main bot file to start the application:

python bot.py

The bot will connect to Discord, set up the database (tasks.db), and sync its commands with your specified guild.

🤖 Command Reference
All commands are slash commands and are designed for intuitive use.

/task add <details>: Creates a new task.

/task claim <task_id>: Claims an active task.

/task done <task_id>: Marks a claimed task as complete.

/task unclaim <task_id>: Releases a claimed task, making it active again.

/tasks: Displays the main task board embed.
