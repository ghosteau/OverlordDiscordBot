This is the source code for a discord bot that I coded using various libraries; it utilizes sci-kit learn for text recogniztion to flag spam, and discord.py for building the bot itself.

The bot has various different commands:
____________________________________________________________________
  chatmute       Used to mute users from text chats
  
  chatunmute     Used to unmute users from text chats
  
  help           Shows this message
  
  info           Credits and information about Overlord
  
  killcount      Check how many spam messages I have terminated
  
  voicemute      Used to mute users in their current voice channel
  
  voicemuteall   Used to mute all users in a call except for admins
  
  voiceunmute    Used to unmute users in their current voice channel
  
  voiceunmuteall Used to unmute all users in a call except for admins
  
  warn           A common warn command to warn users
  
  Type %help command for more info on a command.
____________________________________________________________________

As mentioned earlier, this bot was fed data from a pretty common data set called the spam detection data set. From that, me and my friends added extra data to tune the bot's detection capabilities to our needs, so you will need to do that part yourself.


For future updates, I would expect something along the lines of more SQL compatibility to send flagged messages to a server -- thus users who get false flagged can report it a little easier. But it would have to be transparent to the users beforehand that their message data may be used to help train the model.

____________________________________________________________________

3/11/2024 update:

- Added spamcount command -- used to see how many times a user has been flagged for spam
- Added MicrosoftSQL database storage for flagged messages using SQLAlchemy, dictionaries, and pandas dataframes
- Updated logs with user ID to help sniff out cases of username changing
- Fixed an issue with log channel detection, now looks for "server_logs", "discord_logs", "mod_logs", or  "logs" all as viable log channel names

____________________________________________________________________

3/23/2024 quick addition

- Added message ID to the SQL database information sent to have a true primary incrimentive key
