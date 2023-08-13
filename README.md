This project is currently in a very early development stage. I would not recommend using it, and even if you do, there's not much point as stuff is still being added.
Also, it's currently put on hold. (Again)
# BotBuild
An open-source, self-hosted alternative to mainstream Discord bots, written in Python.

It's designed to be easy to use and quick to set up.

Coming later in 2023 (if all goes well)

# Features
As of right now, nothing listed here is properly implemented. Those are all planned features!

## Design philosophy
- Very modular, different components can be toggled depending on which ones you need.
- A user-friendly dashboard running in the browser which allows control over your bot.
- Uses configuration files for the bot setup, allowing quick deployment in a new environment.

## Modules
BotBuild will support many modules which can be turned on or off depending on your needs, and you can also disable commands which you do not need.

Here is a list of some planned modules:
- Moderation (bans, mutes, etc.) (⚠️)
- Polls (can contain multiple different choices, are anonymous, and use Discord's option buttons) (⚠️)
- Leveling (with support for role rewards, and that is for free!) (❌)
- Reaction roles (highly customizable, can be used for verification systems etc.) (❌)
- Server statistics (messages sent, non-bot members who joined) (❌)
- Welcome/Goodbye messages (can be customized to your heart's content, and used in any channel you want) (⚠️)
- Logging (informs the admins about any moderation actions that have been performed in the server) (❌)
- Channel setup (meme channel allows only messages with media and adds reactions, suggestion channel converts messages into suggestions, and allows voting) (⚠️)
- Games (canvas like r/place, server economy, etc.) (❌)
- Giveaways (chooses a random winner, can check for conditions such as having sent enough messages, being in the server for long enough etc.) (❌)
- Utilities (a shit ton of commands which perform various functions, but do not fit into any of the other categories) (❌)
- Support for external APIs (you need to configure the access on your own, and some of these APIs might need you to pay a fee to use them) (❌)
- Custom commands (there can be as much as your computer/server can handle, and they can use a versatile variable system, perform actions, access third-party APIs etc.) (❌)

### Status
✔️ - Implemented as stable

⚠️ - Implemented as unstable/experimental (Turned off by default, can experience bugs, crashes, are a work-in-progress)

❌ - Not implemented

## High customizablity
Almost every aspect of your bot can be configured the way YOU want it to work.

As mentioned before, the components used can be toggled on or off, and using the GUI or config file, you can alter how the work of individual commands performs.

# Dependencies
This list may be expanded in the future, as the tool is still in a planning stage, and I haven't decided which modules to use yet.

- Flask (used to host the dashboard)
- discord.py (for bot backend)

# Limitations
Currently the bot's access is planned to be limited to just one server, however this may change in the future.
