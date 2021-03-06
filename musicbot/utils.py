from config import config

# A dictionary that remembers which guild belongs to which audiocontroller
guild_to_audiocontroller = {}


def get_guild(bot, command):
    """Gets the guild a command belongs to. Useful, if the command was sent via pm."""
    if command.guild is not None:
        return command.guild
    for guild in bot.guilds:
        for channel in guild.voice_channels:
            if command.author in channel.members:
                return guild
    return None


async def send_message(ctx, message):
    await ctx.send("```\n" + message + "\n```")


async def connect_to_channel(guild, dest_channel_name, ctx, switch=False, default=True):
    """Connects the bot to the specified voice channel.

        Args:
            guild: The guild for witch the operation should be performed.
            switch: Determines if the bot should disconnect from his current channel to switch channels.
            default: Determines if the bot should default to the first channel, if the name was not found.
    """
    for channel in guild.voice_channels:
        if str(channel.name).strip() == str(dest_channel_name).strip():
            if switch:
                try:
                    await guild.voice_client.disconnect()
                except:
                    await send_message(ctx, config.NOT_CONNECTED_MESSAGE)

            await channel.connect()
            return

    if default:
        try:
            await guild.voice_channels[0].connect()
        except:
            await send_message(ctx, config.DEFAULT_CHANNEL_JOIN_FAILED)
    else:
        await send_message(ctx, config.CHANNEL_NOT_FOUND_MESSAGE + str(dest_channel_name))


async def is_connected(ctx):
    try:
        voice_channel = ctx.guild.voice_client.channel
        print(voice_channel)
        return voice_channel
    except:
        return None


def _js_parseInt(string):
    return int(''.join([x for x in string if x.isdigit()]))


def YTDurationToSeconds(duration):
    match = re.match(
        'PT(\d+H)?(\d+M)?(\d+S)?', duration).groups()
    hours = _js_parseInt(match[0]) if match[0] else 0
    minutes = _js_parseInt(match[1]) if match[1] else 0
    seconds = _js_parseInt(match[2]) if match[2] else 0
    return hours * 3600 + minutes * 60 + seconds
