<img width="450" alt="F35C text" src="https://github.com/user-attachments/assets/cda80099-a8c6-45d1-9f8a-1fac603cab3d">

# Generic, multi-role Discord bot

F-35C is designed for you to easily self-host, and use as a template for your own Discord bot project. The codebase is written to be straightforward, clear, and self-explaining,
accompanied by usage of cogs - which makes adding, updating and removing extensions easier and achievable with no downtime.

To get started, simply click **Use this template**, and select either **Open in Codespace** or **[Create a new repository](https://github.com/new?template_name=F-35C&template_owner=attventures)**.

Quick links: **[Getting Started](#getting-started)** | **[attventures Discord](https://discord.gg/ESJZK8Dkfr)**

## Features

### Overview

Features that are enabled by default, which does not require modifying the codebase. **May still require a simple setup to work accordingly on servers**.

Default:

- Basic **economy**
  - Daily paycheck
  - Transfer funds
- Basic **fun**
  - http cat
- Basic **settings**
  - mod action logging channel
  - toggle mod action logging
- **General**
  - ping

These features requires you to input tokens, or make changes (adding/modifying) to the codebase:

- AI chats in DMs and channels specified as AI channels. **Requires you to input your own Groq API key**.
- Evaluate each message's toxicity and insult score, and take automated actions. **Requires you to enter your own Google Cloud token with Perspective API enabled**.

## Getting started

### Installation and running

1. Create an application at the [Discord Developer Portal](https://discord.com/developers/applications).
2. Enable all intents under the Bot tab.
3. Get the token for your bot. **Please keep this at a safe place, Discord will notify you if it's web scrapers found your TOKEN online. If so, your existing token will no longer work, and you'll need to generate a new one**.
4. On this repo page, click on **Use this template**, then select **[Create a new repository](https://github.com/new?template_name=F-35C&template_owner=attventures)**.
5. Enter the details of your new repo.
6. Clone your repo into your local machine
7. Inside the project directory, open `.env` and enter your bot token
8. Run the `main.py` script to start the bot

### Cogs

>[!NOTE]
>Certain cogs need other cogs to function as intended. It is recommended to **not modify or delete** the default cogs unless you know what you are doing.

#### How it works in a nutshell

Read more about cogs [here](https://docs.pycord.dev/en/stable/ext/commands/cogs.html). Cogs that are enabled by default in startup are listed inside `config.json`, under **extensions**. The name of each extension mirrors its filename (eg: general.py) but without the .py extension. The files are stored under the `/cogs` subdirectory.

#### Adding/removing cogs

To add a new cog inside this bot, simply move the Python file into the `/cogs` subdirectory, and add the name of the file into the **extensions** list. The cog will be loaded automatically on the next bot startup. Certain cogs may require you to **make some changes to the codebase in general**. Removing a cog is basically done with the same steps but in reverse.

----

**F-35C** | **©[attventures](https://github.com/attventures)**
