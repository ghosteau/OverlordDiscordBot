import discord
from discord.ext import commands
import OverlordLOG1
import OverlordT
import pandas as pd
from sqlalchemy import create_engine, exc
import asyncio

# Note: this project does not use real Discord user info at all, including for training models
# Do /terms to see the terms of use and privacy policy

spam_counts = {}

def run_discord_bot():
    """
    I highly suggest you use an env variable for storing the bot token, as it is generally safer
    If you suspect somebody has taken your token, report it and change it immediately
    """
    TOKEN = None

    # Emergency secondary check for token --> advisable to use env variable before this
    if TOKEN is None:
        Response = input("Please input your token or else the bot cannot run. Enter 0 to exit. ")

        if Response == 0:
            print("Exiting Overlord...")
            quit(0)
        else:
            TOKEN = Response

    intents = discord.Intents.default()
    intents.message_content = True
    intents.presences = True
    intents.members = True
    spam_count = 0
    SQLToggle = False
    ModelNumber = 0
    connection_string = None
    # % sign as command prefix is depricated, slash commands are now fully supported
    bot = commands.Bot(command_prefix = "%", intents = intents, case_insensitive = True)

    @bot.event
    async def on_ready():
        await bot.tree.sync()
        print(f"{bot.user} is now running!")

    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)
        user_id = int(message.author.id)
        channel_id = int(message.channel.id)
        message_time = str(message.created_at.strftime('%Y-%m-%d %H:%M:%S UTC'))
        message_id = str(message.id)

        nonlocal spam_count
        if ModelNumber == 0:
            spam_flag = False
        if ModelNumber == 1:
            spam_flag = OverlordLOG1.log1_prediction(user_message)
        if ModelNumber == 2:
            spam_flag = OverlordT.t_prediction(user_message)

        if spam_flag and not message.author.guild_permissions.administrator:
            spam_count += 1
            spam_counts[username] = spam_counts.get(username, 0) + 1
            print("Spam detected -- console log")
            await message.delete()

            message_dict = {"Username": [username],
                            "Message": [user_message],
                            "Channel": [channel],
                            "User ID": [user_id],
                            "Channel ID": [channel_id],
                            "Message Time": [message_time],
                            "Message ID": [message_id]}

            if SQLToggle == True:
                message_data = pd.DataFrame.from_dict(message_dict)
                message_data.to_sql("Flagged_Messages", con = engine, if_exists = "append", index = False)


            log_message = discord.Embed(
                color = discord.Color.dark_theme(),
                description = f"""
                :desktop: Channel: #{channel}
                :person_walking: Message by: {message.author.mention} 
                :card_index: User ID: {user_id}
                    
                :scroll: Message: {user_message}
                    
                :clock1: Time logged: {message.created_at.strftime('%Y-%m-%d %H:%M:%S UTC')}
                """,
                title = "Overlord -- Spam Log :rotating_light:"
            )
            log_channel_names = ["server_logs", "discord_logs", "mod_logs", "logs", "logging"]

            for channel_name in log_channel_names:
                log_channel = discord.utils.get(message.guild.channels, name = channel_name)
                if log_channel:
                    break

            if log_channel:
                await log_channel.send(embed = log_message)
            else:
                guild = message.guild
                overwrites = {
                    guild.default_role: discord.PermissionOverwrite(read_messages = False),
                    guild.me: discord.PermissionOverwrite(read_messages = True)
                }
                log_channel = await guild.create_text_channel("server_logs", overwrites=overwrites)
                await log_channel.send("Log channel created.")
                await log_channel.send(log_message)

            await message.channel.send(
                "My algorithm has detected spam and deleted a message. For questions, contact my developer, Ghosteau."
            )

        await bot.process_commands(message)


    @bot.hybrid_command(name = "helpme", help = "A list of Overlord commands and information", arguments = "None")
    async def helpme(ctx):
        embed = discord.Embed(
            color = discord.Color.dark_theme(),
            description = """
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
            """,
            title = "Overlord -- Help & Information"
        )
        embed.set_footer(text="Thank you for using Overlord!")
        embed.set_author(name="The Overlord Team")

        await ctx.send(
            embed = embed
        )

    @bot.hybrid_command(name = "info", help = "Credits and information about Overlord", arguments = "None")
    async def info(ctx):
        embed = discord.Embed(
            color = discord.Color.dark_theme(),
            description = """
            **Welcome to Overlord, a Discord bot designed by Ghosteau.**
            *Ghosteau's GitHub*: https://github.com/ghosteau
            *Project GitHub*: https://github.com/ghosteau/OverlordDiscordBot
            
            This bot is a Discord security application that utilizes machine learning solutions to detect spam and scam, while also leveraging runnable commands to make server moderation easier and more personalized for everyone.
            """,
            title = "Overlord -- A Machine Learning Solution"
        )
        embed.set_footer(text = "Thank you for using Overlord!")
        embed.set_author(name = "The Overlord Team")

        await ctx.send(
            embed = embed
        )

    @bot.hybrid_command(name = "terms", help = "Shows terms of use for Overlord", arguments = "None")
    async def info(ctx):
        embed = discord.Embed(
            color=discord.Color.dark_theme(),
            description="""
                Hello,

                Thank you for using Overlord! This bot is a serious passion project of mine that has truly ignited me to learn and create something that, hopefully, can be of benefit to the Discord community – and if not, at the very least it is something I found a lot of enjoyment in developing.
                 
                Overlord was created because, while I understand there are many amazing security Discord bots out there, as an AI engineer early in my career, I have often thought of how I can aspire to create an innovative application leveraging machine learning as a dynamic solution to a dynamic problem. Countless times, I have found scammers and spammers in Discord servers taking advantage of people publicly in Discord servers; the audacity has gone along far too long. Welcome to world of Overlord.
                
                While I look to provide a quality application, I would also like to lay out some terms of use for the sake of keeping the Overlord project strong and well.
                
                **--------------------------------------------------------------------------------------------------------------------------------------------------------------------**

                **The Overlord Team holds zero accountability for malicious use of the Overlord bot.**
                *We understand this is a publicly downloadable project as of now. We want this project to be beneficial to everyone, but in the case someone manages to use it improperly, we hold zero responsibility for any sorts of damages, money lost, etc… this program has no warranty and is given “as is”.*
                
                **The Overlord Team will NOT collect your data.**
                *Overlord is not a project intended to scrape or mine data – we believe data privacy is a very important factor in modern applications, and we are committed to this idea. We do have SQL support for our bot to directly track spam, but none of this data is ever collected by The Overlord Team and users invoking this feature must let their server population(s) know in accordance with Discord policy; we are not responsible for servers utilizing this functionality and logging your spam data, but please note The Overlord Team itself will NEVER take your personal data.*
                
                **Malicious use of the Overlord bot is prohibited by The Overlord Team.**
                *The Overlord Team is committed to being used for safety purposes. Use of Overlord for malicious intent is completely prohibited and may result in The Overlord Team sanctioning your access to the program. Malicious intent is constituted as embedding malware, using Overlord to push scam, spam, or explicit content, using Overlord to peddle hate speech, or things that may generally be seen as “harmful” to Discord dictated by The Overlord Team.*
                
                **The Overlord Team has the absolute right to update the terms of use.**
                *If the Overlord Team sees fit, we may change the terms of use at any time. This will be done with the best interests of the community and Overlord in mind.*
                
                **The Overlord Team has a complete right to all community contributions.**
                *The Overlord project serves as a unique opportunity to have publicly available source code. With this, we must reiterate community contributions, when accepted and integrated into Overlord, fall under the full ownership of The Overlord Team.*
                
                **The Overlord Team has the right to hide Overlord source code from the public.**
                *Remaining open-source can often be challenging especially when leveraging machine learning models and often having to pay for server hosting fees. At any time, we have the right to revoke this open-source status if the need is felt; this includes the right to hide certain commands for the sake of monetization, or as a means to keep certain aspects of the codebase classified.*
                """,
            title = "Overlord -- Terms of Use"
        )
        embed.set_footer(text="Thank you for using Overlord!")
        embed.set_author(name="The Overlord Team")

        await ctx.send(
            embed = embed
        )

    @bot.hybrid_command(name = "sqlsupport", help = "The command to toggle SQL support", arguments = "None")
    async def SQLSupport(ctx):
        if ctx.author.guild_permissions.administrator:
            nonlocal SQLToggle
            nonlocal connection_string
            if SQLToggle == True:
               SQLToggle = False
               await ctx.send(
                    "SQL support has been toggled to **OFF**."
                )
            else:
                if connection_string is None:
                    await ctx.author.send("Please provide a valid SQL connection string. Do not share this.")

                    def check(msg):
                        return msg.author == ctx.author and isinstance(msg.channel, discord.DMChannel)

                    try:
                        msg = await bot.wait_for("message", check = check, timeout = 60.0)
                        connection_string = msg.content
                        engine = create_engine(connection_string, echo = True)
                    except asyncio.TimeoutError:
                        await ctx.author.send("Conversation timed out! Please try again.")
                        SQLToggle = False
                        connection_string = None
                        return
                    except exc.ArgumentError:
                        await ctx.author.send("Connection failed! Try again.")
                        SQLToggle = False
                        connection_string = None
                        return

                    SQLToggle = True
                    await ctx.send(
                    "SQL support has been toggled to **ON**."
                    )
        else:
            await ctx.send(
                "You don't have necessary permissions to use this command."
            )

    @bot.hybrid_command(name = "spamcount", help = "Check how many spam messages a user has sent", arguments = "Username")
    async def spam_count_command(ctx, user: discord.Member):
        if ctx.author.guild_permissions.administrator:
            user_username = str(user)
            count = spam_counts.get(user_username, 0)
            await ctx.send(f"{user.display_name} has sent {count} spam message(s).")
        else:
            await ctx.send("You don't have the necessary permissions to use this command.")

    @bot.hybrid_command(name = "killcount", help = "Check how many spam messages Overlord has terminated")
    async def kill_count(ctx):
        await ctx.send(f"My total number of spam messages deleted: **{spam_count}**.")

    @bot.hybrid_command(name = "voicemute", help = "Used to mute users in their current voice channel")
    async def voicemute(ctx, user: discord.Member):
        if ctx.author.guild_permissions.mute_members:
            if user.voice and user.voice.channel:
                await user.edit(mute = True)
                await ctx.send(f"{user.display_name} has been muted for voice channels.")
            else:
                await ctx.send(f"{user.display_name} is not in a voice channel.")
        else:
            await ctx.send("You don't have the necessary permissions to use this command.")

    @bot.hybrid_command(name = "voiceunmute", help = "Used to unmute users in their current voice channel")
    async def voiceunmute(ctx, user: discord.Member):
        if ctx.author.guild_permissions.mute_members:
            if user.voice and user.voice.channel:
                await user.edit(mute = False)
                await ctx.send(f"{user.display_name} has been unmuted for voice channels.")
            else:
                await ctx.send(f"{user.display_name} is not in a voice channel.")
        else:
            await ctx.send("You don't have the necessary permissions to use this command.")

    @bot.hybrid_command(name= "voicemuteall", help = "Used to mute all users in a call except for admins", arguments = "None")
    async def voicemuteall(ctx):
        if ctx.author.guild_permissions.administrator:
            if ctx.author.voice and ctx.author.voice.channel:
                for member in ctx.author.voice.channel.members:
                    if not member.guild_permissions.administrator:
                        await member.edit(mute = True)

                await ctx.send(f"All members in {ctx.author.voice.channel.name} muted, except for admins.")
            else:
                await ctx.send("You need to be in a voice channel to use this command.")
        else:
            await ctx.send("You don't have the necessary permissions to use this command.")

    @bot.hybrid_command(name = "voiceunmuteall", help = "Used to unmute all users in a call except for admins")
    async def voiceunmuteall(ctx):
        if ctx.author.guild_permissions.administrator:
            if ctx.author.voice and ctx.author.voice.channel:
                for member in ctx.author.voice.channel.members:
                    if not member.guild_permissions.administrator:
                        await member.edit(mute = False)

                await ctx.send(f"All members in {ctx.author.voice.channel.name} unmuted, except for admins.")
            else:
                await ctx.send("You need to be in a voice channel to use this command.")
        else:
            await ctx.send("You don't have the necessary permissions to use this command.")

    @bot.hybrid_command(name="chatmute", help = "Used to mute users from text chats")
    async def chatmute(ctx, user: discord.Member):
        if ctx.author.guild_permissions.manage_roles:
            for channel in ctx.guild.text_channels:
                await channel.set_permissions(user, send_messages = False)

            await ctx.send(f"{user.display_name} has been muted in text channels.")
        else:
            await ctx.send("You don't have the necessary permissions to use this command.")

    @bot.hybrid_command(name = "chatunmute", help = "Used to unmute users from text chats")
    async def chatunmute(ctx, user: discord.Member):
        if ctx.author.guild_permissions.manage_roles:
            for channel in ctx.guild.text_channels:
                await channel.set_permissions(user, send_messages = True)

            await ctx.send(f"{user.display_name} has been unmuted in text channels.")
        else:
            await ctx.send("You don't have the necessary permissions to use this command.")

    @bot.hybrid_command(name= "warn", help = "A common warn command to warn users")
    async def warn(ctx, user: discord.Member, *, reason=""):
        if ctx.author.guild_permissions.mute_members:
            if reason == "":
                reason = "no reason specified"

            await ctx.send(f"**{user.mention}** has been warned for **{reason}**.")
        else:
            await ctx.send("You don't have the necessary permissions to use this command.")

    @bot.hybrid_command(name = "modelselection", help = "Used to switch or disable AI detection models")
    async def modelselection(ctx, toggle_number):
        nonlocal ModelNumber
        try:
            toggle_number = int(toggle_number)
        except TypeError:
            await ctx.send("Please input an integer for the `modelselection` command.")

        if ctx.author.guild_permissions.administrator:
            if toggle_number == ModelNumber:
                await ctx.send("I am already set to that setting.")
            else:
                ModelNumber = toggle_number
                if toggle_number == 0:
                    await ctx.send("Overlord AI detection has been **disabled**.")

                if toggle_number == 1:
                    await ctx.send("Overlord AI detection has been enabled -- model is set to **Overlord-LOG1**.")

                if toggle_number == 2:
                    await ctx.send("Overlord AI detection has been enabled -- model is set to **Overlord-T**.")

                if toggle_number > 2 or toggle_number < 0:
                    await ctx.send("Model selection failed -- invalid number for model selection.")
        else:
            await ctx.send("You don't have the necessary permissions to use this command.")


    bot.run(TOKEN)