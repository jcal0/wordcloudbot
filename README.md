# Discord Word Frequency Bot

This Discord bot downloads a specified number of messages across all channels in a server and calculates the top 10 most frequently used words.

## Installation

1. Clone this repository:

```bash
git clone https://github.com/yourusername/wordcloudbot.git
```

2. Change project directory:

```
cd wordcloudbot
```

3. Create a virtual environment:

```
python -m venv venv
```

4. Activate the virtual environment:

- On windows:

```
venv\Scripts\activate
```

- On MacOS and Linux:
```
venv\Scripts\activate
```

5. Install required packages:
```
pip install -r requirements.txt
```

Usage:

1. Create a .env file in the project directory and add your Discord bot token:
```
DISCORD_TOKEN=your-bot-token
```

2. Run the bot:
```
python script.py
```

3. In Discord, use the -wordcloud command to generate the top 10 most frequently used words:
```
-wordcloud

```

