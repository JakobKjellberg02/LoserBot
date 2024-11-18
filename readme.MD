# LoserBot

![](https://media.tenor.com/WKWonIB6gjIAAAAM/police-siren-siren.gif)

LoserBot is a simple Discord bot that records a ragequit from an user to display for the whole server.

## Getting started

1. If you don't know how to get a bot key, follow the tutorial at [https://www.writebots.com/discord-bot-token/](https://www.writebots.com/discord-bot-token/)
2. Clone the repo
```sh
   git clone https://github.com/JakobKjellberg02/LoserBot.git
   ```
3. Setup Python 3.9.10 virtual enviroment
```sh
python3 -m venv <env_name>
source <env_name>/bin/activate
(<env_name>) pip install -r requirements.txt
```
4. Create ```.env``` for API keys
```
nano .env
/* Opens .env with Nano
DISCORD_TOKEN=<secret_key>
```
5. Run ```__main.py__```
```
(<env_name>) python3 __main__.py
```

## Usage
Run the command ```!help``` to view all available commands

```
!loss @user USERNAME_EUNE - Record a rage quit loss for specific user e.g. Mini aram
!losses @user - WALL OF SHAME for specific user (note: minikillerj might have bugged it)
!losses  - WALL OF SHAME for the server
```

## Requirments
```python
aiohappyeyeballs==2.4.3
aiohttp==3.11.2
aiosignal==1.3.1
async-timeout==5.0.1
attrs==24.2.0
certifi==2024.8.30
discord.py==2.4.0
exceptiongroup==1.2.2
frozenlist==1.5.0
h11==0.14.0
idna==3.10
multidict==6.1.0
outcome==1.3.0.post0
propcache==0.2.0
PySocks==1.7.1
python-dotenv==1.0.1
selenium==4.26.1
sniffio==1.3.1
sortedcontainers==2.4.0
trio==0.27.0
trio-websocket==0.11.1
typing_extensions==4.12.2
urllib3==2.2.3
websocket-client==1.8.0
wsproto==1.2.0
yarl==1.17.2
```
