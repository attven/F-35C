<img width="450" alt="F35C text" src="https://github.com/user-attachments/assets/cda80099-a8c6-45d1-9f8a-1fac603cab3d">

# Generic, multirole Discord bot

F-35C is designed for you to easily self-host, and use as a template for your own Discord bot project. The codebase is written to be straightforward, clear, and self-explaining,
accompanied by usage of cogs - which makes adding, updating and removing extensions easier and achievable with no downtime.

To get started, simply click **Use this template**, and select either **Open in Codespace** or **[Create a new repository](https://github.com/new?template_name=F-35C&template_owner=attventures)**.

Quick links: **[Getting Started](#getting-started)**

## Features

### Default

Features that are enabled by default, which does not require modifying the codebase. **May still require a simple setup to work accordingly on servers**.

- Basic security
  - Flag addition of unverified bots
- Basic global economy
  - Claim daily cash
  - Transfer cash to other users
  - Farm Bitcoin (for cash)
- Welcome messages to new users
- Get random pictures
  - cats
  - dogs
  - hamsters
  - http cat
 - Per-server settings (in progress)

### Optional

These features requires you to input tokens, or make changes (adding/modifying) to the codebase.

- AI chats in DMs and channels specified as AI channels. **Requires you to input your own Groq API key**.
- Evaluate each message's toxicity and insult score, and take automated actions. **Requires you to enter your own Google Cloud token with Perspective API enabled**.

## Getting started

### Installation and running

1. Create an application at the [Discord Developer Portal](https://discord.com/developers/applications).
2. Get the token for your bot. **Please keep this at a safe place, Discord will notify you if it's web scrapers found your TOKEN online. If so, your existing token will no longer work, and you'll need to generate a new one**.
3. On this repo page, click on **Use this template**, then select **[Create a new repository](https://github.com/new?template_name=F-35C&template_owner=attventures)**.
4. Enter the details of your new repo.
5. Clone your repo into your local machine
6. Inside the project directory, open `.env` and enter your bot token
7. Run the `main.py` script to start the bot

----

**F-35C** | **©[attventures](https://github.com/attventures)**
