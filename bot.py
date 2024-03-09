import discord
from discord.ext import commands
import SpamRecognizerModel

# This does not use real message data from Discord users -- rather emulated responses for ethical reasons

def run_discord_bot():
    TOKEN = "put your token here"  # This is to be kept SECRET!!!
    intents = discord.Intents.default()
    intents.message_content = True
    intents.presences = True
    intents.members = True
    spam_count = 0

    bot = commands.Bot(command_prefix = "%", intents = intents, case_insensitive = True)

    @bot.event
    async def on_ready():
        print(f"{bot.user} is now running!")

    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        nonlocal spam_count  # Use the global variable
        spam_flag = SpamRecognizerModel.model_prediction(user_message)
        if spam_flag and not message.author.guild_permissions.administrator:
            spam_count += 1
            print("Spam detected -- console log")
            await message.delete()

            log_message = f"Spam detected in *#{channel}* by {message.author.mention}: `{user_message}` -- {message.created_at.strftime('%Y-%m-%d %H:%M:%S UTC')}"
            log_channel = discord.utils.get(message.guild.channels, name = "server_logs")

            if log_channel:
                await log_channel.send(log_message)
            else:
                guild = message.guild
                overwrites = {
                    guild.default_role: discord.PermissionOverwrite(read_messages = False),
                    guild.me: discord.PermissionOverwrite(read_messages = True)
                }
                log_channel = await guild.create_text_channel("server_logs", overwrites=overwrites)
                await log_channel.send("Log channel created.")

            await message.channel.send(
                "My algorithm has detected spam and deleted the message, for questions contact my developer  `@Ghosteau`."
            )

        await bot.process_commands(message)  # This line should be inside on_message event

    @bot.command(name = "info", help = "Credits and information about Overlord")
    async def info(ctx):
        await ctx.send(
            "Developed by  `@Ghosteau`  -->  **GitHub**: https://github.com/ghosteau  ||  This bot is a personal security helper that utilizes machine learning solutions to detect spam, while also using commands to moderate"
        )

    @bot.command(name = "killcount", help = "Check how many spam messages I have terminated")
    async def kill_count(ctx):
        await ctx.send(f"My total number of spam messages deleted: {spam_count}")

    @bot.command(name = "voicemute", help = "Used to mute users in their current voice channel")
    async def voicemute(ctx, user: discord.Member):
        if ctx.author.guild_permissions.mute_members:
            if user.voice and user.voice.channel:
                await user.edit(mute = True)
                await ctx.send(f"{user.display_name} has been muted for voice channels.")
            else:
                await ctx.send(f"{user.display_name} is not in a voice channel.")
        else:
            await ctx.send("You don't have the necessary permissions to use this command.")

    @bot.command(name = "voiceunmute", help = "Used to unmute users in their current voice channel")
    async def voiceunmute(ctx, user: discord.Member):
        if ctx.author.guild_permissions.mute_members:
            if user.voice and user.voice.channel:
                await user.edit(mute = False)
                await ctx.send(f"{user.display_name} has been unmuted for voice channels.")
            else:
                await ctx.send(f"{user.display_name} is not in a voice channel.")
        else:
            await ctx.send("You don't have the necessary permissions to use this command.")

    @bot.command(name= "voicemuteall", help = "Used to mute all users in a call except for admins")
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

    @bot.command(name = "voiceunmuteall", help = "Used to unmute all users in a call except for admins")
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

    @bot.command(name="chatmute", help = "Used to mute users from text chats")
    async def chatmute(ctx, user: discord.Member):
        if ctx.author.guild_permissions.manage_roles:
            for channel in ctx.guild.text_channels:
                await channel.set_permissions(user, send_messages = False)

            await ctx.send(f"{user.display_name} has been muted in text channels.")
        else:
            await ctx.send("You don't have the necessary permissions to use this command.")

    @bot.command(name = "chatunmute", help = "Used to unmute users from text chats")
    async def chatunmute(ctx, user: discord.Member):
        if ctx.author.guild_permissions.manage_roles:
            for channel in ctx.guild.text_channels:
                await channel.set_permissions(user, send_messages = True)

            await ctx.send(f"{user.display_name} has been unmuted in text channels.")
        else:
            await ctx.send("You don't have the necessary permissions to use this command.")

    @bot.command(name= "warn", help = "A common warn command to warn users")
    async def warn(ctx, user: discord.Member, *, reason=""):
        if ctx.author.guild_permissions.mute_members:
            await ctx.message.delete()

            if reason == "":
                reason = "no reason specified"

            await ctx.send(f"**{user.mention}** has been warned for **{reason}**.")
        else:
            await ctx.send("You don't have the necessary permissions to use this command.")

    bot.run(TOKEN)