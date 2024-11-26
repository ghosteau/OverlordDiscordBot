# Overlord Discord Bot -- Official Codebase

> **Note**: Due to file size limitations, the Overlord-T pre-trained model could not be uploaded to GitHub. You can access it directly via Hugging Face using the link below:

[**Hugging Face link for Overlord-T Model**](https://huggingface.co/ghosteau/OverlordT/tree/main)

---

## Commands and Features
Below is a list of commands supported by Overlord:

- `helpme`: Displays a comprehensive list of commands and their descriptions.
- `info`: Provides general information and credits for Overlord.
- `terms`: Displays Overlord's official terms of use.
- `chatmute <user>`: Mutes a user in all text channels.
- `chatunmute <user>`: Unmutes a user in all text channels.
- `voicemuteall`: Mutes all users in a voice channel (excluding admins).
- `voiceunmuteall`: Unmutes all users in a voice channel.
- `voicemute <user>`: Mutes a specific user in a voice channel.
- `voiceunmute <user>`: Unmutes a specific user in a voice channel.
- `warn <user> <reason>`: Sends a warning message to a user.
- `killcount`: Displays the total number of messages terminated by Overlord.
- `spamcount <user>`: Shows the total number of terminated messages for a specific user.
- `sqlsupport`: Toggles SQL support for the spam message registry.
- `modelselection <modelnumber>`: Toggles AI detection modes:
  - `0`: Disable AI detection.
  - `1`: Use Overlord-LOG1 (legacy model).
  - `2`: Use Overlord-T (state-of-the-art model).

---

## Update Log

### **3/11/2024 Update**
- **New Feature**: Added the `spamcount` command to track the number of times a user has been flagged for spam.
- **Database Integration**: Introduced Microsoft SQL database storage for flagged messages using SQLAlchemy, dictionaries, and pandas DataFrames.
- **Enhanced Logging**: User ID added to logs to track cases of username changes.
- **Bug Fix**: Improved log channel detection to support multiple naming conventions (“server_logs,” “discord_logs,” “mod_logs,” and “logs”).

### **3/23/2024 Quick Update**
- **Database Improvement**: Added message IDs to the SQL database as a primary incremental key.

### **7/25/2024 Major Update**
- **Slash Command Support**: Full support for slash commands; deprecated `%` prefix.
- **AI Detection Modes**: Introduced three modes for AI detection:
  - **Off Mode**: Disables detection.
  - **Overlord-LOG1**: Legacy model with reliable performance.
  - **Overlord-T**: Premium state-of-the-art model designed for continuous updates.
- **Help Command Overhaul**: Improved `helpme` command to be more user-friendly and comprehensive.
- **Organized Logs**: Enhanced log organization and usability for developers and users.
- **Terms of Use**: Added `/terms` slash command to display Overlord’s official terms of use.
- **Codebase Refactoring**: Optimized codebase structure for easier maintenance and development.
- **SQL Integration Slash Command**: Added slash command for toggling SQL support, ensuring compliance with Discord policies and Overlord terms of use.
- **Transformer Model Link**: Added Hugging Face link for Overlord-T due to file size limitations.

---

