# listen.py - code by Rye

# This file will contain the discord event listeners
# and the response the bot will have to them
from nextcord.ext import commands

import runtime
from runtime import SnowBot
from warehouse.classes import cGuild
import nextcord


class Execution(commands.Cog):
    def __init__(self, bot: SnowBot):
        self.bot: SnowBot = bot
        self.dba = self.bot.dba
        self.__status = 'and Listening'
        self.guild_join_msg = '***HEWWO?!? :sparkles:***\nI am Kyrie... yeah that\'s it. :D\n\n' \
                              'Oh yeah! I enabled some default settings, and I also set this channel' \
                              ' to be my channel to send important messages! You can check the "sectors"' \
                              ' enabled by default by doing `.guild_feat`.'

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot: SnowBot
        print(f'Logged in as [{self.bot.user}] successfully.')
        await self.bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.watching,
                                                                  name=str(self.__status)),
                                       status=nextcord.Status.online)
        for guild in self.bot.guilds:
            self.bot.cguilds.append(cGuild(guild.id, guild.name, self.dba))
        return

    @commands.Cog.listener()
    async def on_guild_update(self, before, after):
        if before.name != after.name:
            for cg in self.bot.cguilds:
                if cg.gid == after.id:
                    cg.name = after.name
                else:
                    continue

    @commands.command()
    @commands.is_owner()
    async def features(self, ctx):
        cg = self.bot.get_cguild(ctx.guild.id)
        await ctx.send(cg.get_feat())
        await ctx.message.delete()

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        user = await self.bot.fetch_user(int(self.bot.owner_id))
        user_dm = await user.create_dm()
        await user_dm.send(f'I joined a new server! Yay!\nJoined server: {guild.name}\nGuild ID: {guild.id}')
        print(f'{self.bot.user} joined a new Guild! It joined: ({guild.name})(ID:{guild.id})')
        announce = None
        if guild.system_channel:
            announce = guild.system_channel
        else:
            for channel in guild.text_channels:
                if channel.permissions_for(guild.me).send_messages:
                    announce = channel
                    break
        if announce:
            await announce.send(self.guild_join_msg)
            self.bot.cguilds.append(cGuild(guild.id, guild.name, self.dba, announce=announce.id))


def setup(bot):
    bot.add_cog(Execution(bot))
