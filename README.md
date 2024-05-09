# Telegram Joke Bot

This Telegram bot is designed to send scheduled jokes to users. It utilizes the aiogram library for Telegram bot development and MongoDB for data storage.

## Features

- **Scheduled Jokes**: Admins can add jokes to be sent to users at specified time (time is specified in bot.py file).
- **Admin Panel**: Administrators have access to an admin panel to add jokes and send custom messages.
- **User Management**: Users can subscribe and unsubscribe from receiving jokes.

## Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your/repository.git
   cd repository
   ```

2. **Install Dependencies**:
   I recommend using a virtual environment, here is an example for win:
   ```bash
   python -m venv venv
   . venv/scripts/activate
   ```

   ```bash
   pip install -r requirements.txt
   ```

3. **Configuration**:
   - Create a `.env` file based on the provided `.env.example`:
   ```bash
   TOKEN='telegram bot token'
   MONGO_URL='localhost'
   ADMIN_ID='your telegram token'
   ```

4. **Run the Bot**:
   ```bash
   python bot.py
   ```
   OR you can use docker-compose if you know how to do that.

## Usage

### ADMIN Commands

- `/admin`: Access the admin panel.
- `/add_joke`: Add a new joke to the database.
- `/send_custom_message`: Send a custom message to all users.

### USER Commands

- `/start`: Start the bot and subscribe to receive jokes.
- `/stop`: Unsubscribe from receiving jokes.
- `/help`: Display help message.


## Contributors

- Nikita Nesterenko (@Nikita_irl)

## License

Allowed for non-profit use.