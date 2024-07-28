# Overlord Discord Bot -- Official Codebase
*Quick note: due to some file sizes, particularly with the transformer models, the Overlord-T pre-save could not be uploaded on GitHub. You can use the Hugging Face link below to access the Overlord-T model directly instead.*

**Hugging Face link for Overlord-T Model**: https://huggingface.co/ghosteau/OverlordT/tree/main

____________________________________________________________________

**Here is a list of commands and information.**
            
            ```helpme``` shows a list of commands and information
            ```info``` gives general info and credits for Overlord
            ```terms``` shows the official Overlord terms of use
            ```chatmute``` (arguments: user) mutes a user in all text channels
            ```chatunmute``` (arguments: user) unmutes a user in all texts channels
            ```voicemuteall``` mutes all users in a voice channel (excluding admins)
            ```voiceunmuteall``` unmutes all users in a voice channel
            ```voicemute``` (arguments: user) mutes a user in a voice channel
            ```voiceunmute``` (arguments: user) unmutes a user in a voice channel
            ```warn``` (arguments: user, reason) pings and warns a user; general warn command
            ```killcount``` shows how many messages have been terminated by Overlord
            ```spamcount``` (arguments: user) shows total terminated messages for specific user
            ```sqlsupport``` a command to toggle SQL support for spam message registry
            ```modelselection``` (arguments: modelnumber) a command to disable or toggle AI detection; input 0 to disable, 1 to use LOG1, and 2 to use T
            
____________________________________________________________________
*UPDATE LOG*

3/11/2024 update:

- Added spamcount command -- used to see how many times a user has been flagged for spam.
- Added MicrosoftSQL database storage for flagged messages using SQLAlchemy, dictionaries, and pandas dataframes.
- Updated logs with user ID to help sniff out cases of username changing.
- Fixed an issue with log channel detection, now looks for "server_logs", "discord_logs", "mod_logs", or  "logs" all as viable log channel names.

____________________________________________________________________

3/23/2024 quick update:

- Added message ID to the SQL database support to create a true primary incrimentive key.
_____________________________________________________________________

7/25/24 big update:

- Complete support for slash commands now; % prefix support is now deprecated.
- Overlord now has 3 modes for AI detection (via slash command): a toggle off mode, Overlord-LOG1 (old model which still works perfectly fine), and Overlord-T. The T model is going to be our state-of-the-art/premium model going forward, with hopes to continuously update it to provide a dynamic and effective solution.
- Massive update to the help command (now called helpme) to be much more organized and a lot more helpful... as it should be.
- Going along with the helpme command addition and updates, the logs and the info command are also now more organized and informative.
- An official terms of use has been added, which you can read now doing /terms.
- The codebase is now much more organized. This will not effect the average user but it is going to be something that will benefit developers and myself going forward.
- There is now a slash command to toggle SQL support (for your personal SQL servers to track spam logging). Be careful with this functionality and act in accordance with Discord policy and the Overlord terms of use.
- Added a Hugging Face link for the transformer model, Overlord-T, due to file size issues.
_____________________________________________________________________

