**Note:** As of right now, the only thing present in this repository is this readme. Keep in mind, that I also have a game to work on (I'd like to prioritize that, but also work on BotBuild at that time) and IRL stuff to do, so development might take a while. I'd release the first public version when there's some basic stuff ready, laying a foundation for this project. I hope this is understandable!

# BotBuild
An open-source, self-hosted alternative to mainstream Discord bots, written in Python.

It's pretty easy to use and commands are available to use out of the box, more can be added by either coding in your own stuff into the program, or by using the built-in custom command system. I guess you could consider this an open source BotGhost alternative.

# Features
As of right now, nothing listed here is properly implemented. Those are all planned features!

## Design
- Very modular, different components can be toggled depending on which ones you need.
- A user-friendly dashboard made using Tkinter which allows control over your bot.
- Uses configuration files for the bot setup, allowing quick deployment in a new environment.

## Modules
BotBuild will support many modules which can be turned on or off depending on your needs, and you can also disable commands which you do not need.

Here is a list of some planned modules:
- Moderation (bans, mutes, etc.) (❌)
- Polls (can contain multiple different choices, are anonymous, and use Discord's option buttons) (❌)
- Leveling (with support for role rewards, and that is for free!) (❌)
- Reaction roles (highly customizable, can be used for verification systems etc.) (❌)
- Server statistics (messages sent, non-bot members who joined) (❌)
- Welcome/Farewell messages (can be customized to your heart's content, and used in any channel you want) (❌)
- Logging (informs the admins about any moderation actions that have been performed in the guild) (❌)
- Channel setup (meme channel allows only messages with media and adds reactions, suggestion channel converts messages into suggestions, and allows voting) (❌)
- Games (canvas like r/place, server economy, etc.) (❌)
- Giveaways (chooses a random winner, can check for conditions such as having sent enough messages, being in the server for long enough etc.) (❌)
- Utilities (a shit ton of commands which perform various functions, but do not fit into any of the other categories) (❌)
- Custom commands (there can be as much as your computer/server can handle, and they can use a versatile variable system, perform actions, access third-party APIs etc.) (❌)

## High customizablity
Almost every aspect of your bot can be configured the way YOU want it to work.

As mentioned before, the components used can be toggled on or off, and using the GUI or config file, you can alter how the work of individual commands performs.

# Dependencies
- tkinter (for GUI dashboard, optional)
- discord.py (for bot backend)
