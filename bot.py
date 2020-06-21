import discord
import profileRequestor
import json

with open('auth.json') as f:
    auth = json.load(f)
    f.close()
with open('data.json') as f:
    hypixelData = json.load(f)
    f.close()


class DiscordBot(discord.Client):
    def __init__(self, *, loop=None, **options):
        super().__init__(loop=None, **options)
        self.adminRoles = []
        self.applyChannels = []
        self.outChannels = []
        self.levelReqs = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.slayerReqs = [0, 0, 0, 0]
        self.currCmd = discord.Message

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        if message.content.split()[0] == '!ga':
            self.currCmd = message
            for role in self.currCmd.author.roles:
                if role.name in self.adminRoles:
                    await self.admin_user()
                    break

            await self.nonadmin_user()

    async def admin_user(self):
        cmdText = self.currCmd.content.split()
        if cmdText[1] == 'exit':
            await self.currCmd.channel.send('Exited program')
            exit(0)
        #
        if cmdText[1] == 'ping':
            await self.currCmd.channel.send('Pong!')
        #
        #
        #
        if cmdText[1] == 'addAdminRole':
            try:
                self.adminRoles.append(cmdText[2])
            except IndexError:
                await self.ie()
                return

            await self.currCmd.channel.send("```Successfully added admin role '{0}'```".format(cmdText[2]))
        #
        if cmdText[1] == 'removeAdminRole':
            roleExists = 0
            try:
                searchedRole = cmdText[2]
            except IndexError:
                await self.ie()
                return

            for i in range(len(self.adminRoles)):
                if self.adminRoles[i] == searchedRole:
                    self.adminRoles.pop(i)
                    roleExists = 1
            if roleExists:
                await self.currCmd.channel.send("```Removed '{0}' from admin roles```".format(searchedRole))
            else:
                await self.currCmd.channel.send("```'{0}' is not an admin role```".format(searchedRole))
        #
        if cmdText[1] == 'printAdminRoles':
            await self.currCmd.channel.send(self.adminRoles)
        #
        #
        #
        if cmdText[1] == 'addApplyChannel':
            try:
                self.applyChannels.append(cmdText[2])
            except IndexError:
                await self.ie()
                return

            await self.currCmd.channel.send("```Successfully added apply channel '{0}'```".format(cmdText[2]))
        #
        if cmdText[1] == 'removeApplyChannel':
            channelExists = 0
            try:
                searchedChannel = cmdText[2]
            except IndexError:
                await self.ie()
                return

            for i in range(len(self.applyChannels)):
                if self.applyChannels[i] == searchedChannel:
                    self.applyChannels.pop(i)
                    channelExists = 1
            if channelExists:
                await self.currCmd.channel.send("```Removed '{0}' from apply channels```".format(searchedChannel))
            else:
                await self.currCmd.channel.send("```'{0}' is not an apply channel```".format(searchedChannel))
        if cmdText[1] == 'printApplyChannels':
            await self.currCmd.channel.send(self.applyChannels)
        #
        #
        #
        if cmdText[1] == 'addOutChannel':
            try:
                self.outChannels.append(cmdText[2])
            except IndexError:
                await self.ie()
                return

            await self.currCmd.channel.send("```Successfully added output channel '{0}'```".format(cmdText[2]))
        #
        if cmdText[1] == 'removeOutChannel':
            channelExists = 0
            try:
                searchedChannel = cmdText[2]
            except IndexError:
                await self.ie()
                return

            for i in range(len(self.outChannels)):
                if self.outChannels[i] == searchedChannel:
                    self.outChannels.pop(i)
                    channelExists = 1
            if channelExists:
                await self.currCmd.channel.send("```Removed '{0}' from output channels```".format(searchedChannel))
            else:
                await self.currCmd.channel.send("```'{0}' is not an output channel```".format(searchedChannel))
        if cmdText[1] == 'printOutChannels':
            await self.currCmd.channel.send(self.outChannels)
        #
        #
        #
        if cmdText[1] == 'addReqs':
            try:
                reqType = cmdText[2]
            except IndexError:
                await self.ie()
                return

            if reqType == 'level':
                try:
                    self.levelReqs[hypixelData['levelMap'][cmdText[3]]] = int(cmdText[4])
                    await self.currCmd.channel.send(
                        '```Successfully changed {0} level requirement to {1}```'.format(cmdText[3], cmdText[4]))
                except KeyError:
                    await self.ue()
                except ValueError:
                    await self.ve()
                    return
                except IndexError:
                    await self.ie()
                    return

            if reqType == 'slayer':
                try:
                    self.slayerReqs[hypixelData['slayerMap'][cmdText[3]]] = int(cmdText[4])
                    await self.currCmd.channel.send(
                        '```Successfully changed {0} slayer requirement to {1} xp```'.format(cmdText[3], cmdText[4]))
                except KeyError:
                    await self.ue()
                except ValueError:
                    await self.ve()
                    return
                except IndexError:
                    await self.ie()
                    return
        #
        #
        #
        if cmdText[1] == 'levelTypes':
            outStr = '```\n'
            for key in hypixelData['levelMap']:
                outStr += key + '\n'
            outStr += '```'
            await self.currCmd.channel.send(outStr)
        if cmdText[1] == 'slayerTypes':
            outStr = '```\n'
            for key in hypixelData['slayerMap']:
                outStr += key + '\n'
            outStr += '```'
            await self.currCmd.channel.send(outStr)
        if cmdText[1] == 'help':
            await self.currCmd.channel.send('```commands template - !ga [command] [arguments]\n\n'
                                            '𝐏𝐨𝐬𝐬𝐢𝐛𝐥𝐞 𝐜𝐨𝐦𝐦𝐚𝐧𝐝𝐬:\n'
                                            'ping - pings the bot, \'Pong!\' is default answer\n'
                                            'addAdminRole [role] - adds admin role\n'
                                            'removeAdminRole [role] - removes given role from admin roles\n'
                                            'printAdminRoles - prints current admin roles\n'
                                            'addApplyChannel [channel] - adds apply channel\n'
                                            'removeApplyChannel [channel] - removes given channel from apply channels\n'
                                            'printApplyChannels - prints current apply channels\n'
                                            'addOutChannel [channel] - adds output channel\n'
                                            'removeOutChannel [channel] - removes given channel from output channels\n'
                                            'printOutChannels - prints current output channels\n'
                                            'addReqs [type1] [type2] [value]\n'
                                            '   - type1 should be \'level\' or \'slayer\'\n'
                                            '   - to get possible type2 values use one for 2 following commands\n'
                                            '   - value must be an integer! For slayer it indicates needed EXP, not level!\n'
                                            'levelTypes - displays possible values for type2 in addReqs with type1 being \'level\'\n'
                                            'slayerTypes - displays possible values for type2 in addReqs with type1 being \'slayer\'\n'
                                            'help - displays this massage```')

    async def nonadmin_user(self):
        cmdText = self.currCmd.content.split()
        #
        # Only for initializing first admin role (preferably 'admin' or 'owner')
        if len(self.adminRoles) == 0:
            if cmdText[1] == 'addAdminRole':
                try:
                    self.adminRoles.append(cmdText[2])
                except IndexError:
                    await self.ie()
                    return

                await self.currCmd.channel.send("```Successfully added first admin role '{0}'```".format(cmdText[2]))
            if cmdText[1] == 'help':
                await self.currCmd.channel.send('```Type in \'!ga addAdminRole [role]\' to add administrator role```')
                return
        #
        if cmdText[1] == 'apply' and self.currCmd.channel.name in self.applyChannels:
            await self.check_applies()

    async def ie(self):
        await self.currCmd.channel.send('```Not enough arguments! Type \'!ga help\' to display command list```')

    async def ve(self):
        await self.currCmd.channel.send('```Wrong value! Type \'!ga help\' to display command list```')

    async def ue(self):
        await self.currCmd.channel.send('```Unknown argument! Type \'!ga help\' to display command list```')

    async def check_applies(self):
        username = self.currCmd.content.split()[2]
        profileName = self.currCmd.content.split()[3]
        profile = profileRequestor.get_profile(username, profileName)
        if profile == -1:
            await self.currCmd.channel.send("```Couldn't find given user/profile!```")
            return
        playerSlayers = [0, 0, 0, 0]
        for key in hypixelData['slayerMap']:
            if key == 'total':
                continue
            playerSlayers[hypixelData['slayerMap'][key]] = profile['slayer_bosses'][key]['xp']
            playerSlayers[0] += playerSlayers[hypixelData['slayerMap'][key]]

        playerLevels = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for key in hypixelData['levelMap']:
            if key == 'average':
                continue

            if key == 'runecrafting':
                r = 1
            else:
                r = 0

            playerLevels[hypixelData['levelMap'][key]] = self.binary_search(profile['experience_skill_'+key], r)

            if key == 'runecrafting' or key == 'carpentry':
                continue
            playerLevels[0] += playerLevels[hypixelData['levelMap'][key]]
        playerLevels[0] /= 8

        outStr = '```\n'
        outStr += 'Player under consideration: ' + username + ',\nprofile: ' + profileName + '\n\n'
        fillLevelReqs = 1
        for key in hypixelData['levelMap']:
            if self.levelReqs[hypixelData['levelMap'][key]] > playerLevels[hypixelData['levelMap'][key]]:
                outStr += "Player doesn't have high enough " + key + ' level, ' + \
                          str(round(self.levelReqs[hypixelData['levelMap'][key]] - playerLevels[hypixelData['levelMap'][key]], 2)) + \
                          ' more required\n'
                fillLevelReqs = 0
        if fillLevelReqs:
            outStr += 'Player fulfils all skill levels requirements\n'

        fillSlayerReqs = 1
        for key in hypixelData['slayerMap']:
            if self.slayerReqs[hypixelData['slayerMap'][key]] > playerSlayers[hypixelData['slayerMap'][key]]:
                outStr += "Player doesn't have high enough " + key + ' slayer, ' + \
                          str(round(self.slayerReqs[hypixelData['slayerMap'][key]] - playerSlayers[hypixelData['slayerMap'][key]], 2)) + \
                          ' more xp required\n'
                fillSlayerReqs = 0
        if fillSlayerReqs:
            outStr += 'Player fulfils all slayer requirements\n\n'

        outStr += 'Skylea for further checking:\nhttps://sky.lea.moe/stats/' + username + '/' + profileName
        for channel in self.currCmd.guild.channels:
            if channel.name in self.outChannels:
                await channel.send(outStr+'```')

    @staticmethod
    def binary_search(x, r):
        if r:
            arr = hypixelData['runecrafting']
        else:
            arr = hypixelData['default']
        low = 0
        high = len(arr) - 1

        while low <= high:
            mid = (high + low) // 2

            if arr[str(mid)] < x < arr[str(mid + 1)]:
                return mid + (x - arr[str(mid)]) / (arr[str(mid + 1)] - arr[str(mid)])

            elif arr[str(mid)] > x:
                high = mid

            else:
                low = mid - 1


bot = DiscordBot()
bot.run(auth['discordToken'])
