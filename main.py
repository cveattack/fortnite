from auth import auth, endpoints
import shutil
import os
import telebot
from telebot import types
from somecoolstuff import stuff
from checkers import checkers

WHITELIST = ['AthenaCharacter', 'AthenaBackpack',
             'AthenaPickaxe', 'AthenaDance']
API_TOKEN = ''
WHITELISTUNAMES = ['magiclzt', 'liljaba1337', 'GlobalSellerFN']

bot = telebot.TeleBot(API_TOKEN)

bot.set_my_commands([
    telebot.types.BotCommand("/start", "use the checker")
])

auth_code = None


@bot.message_handler(commands=['start'])
def usechecker(message):
    if message.chat.type != "private":
        return

    if message.from_user.username not in WHITELISTUNAMES:
        bot.reply_to(
            message, 'You didnt have accses!')
        return

    msg = bot.reply_to(message, 'creating a login link')

    authclient = auth()
    link = authclient.getauthlink()

    bot.edit_message_text('Follow <a href="{}">this link</a> and login into ur account'.format(
        link), msg.chat.id, msg.id, parse_mode='HTML')
    
    authclient.wait_for_device_code_completion()

    makeapickchecklist = {}
    for i in WHITELIST:
        makeapickchecklist[i] = '❌'

    client = authclient.account
    accountmetadata = authclient.getaccountmetadata()
    bot.edit_message_text(
        f'successfully logged in as {client.name}\n\nchecking info', msg.chat.id, msg.id)
    cosmetics_arrays, cosmetics_name_and_info_arrays, seasonsinfo, cursesinfo = checkers.locker(
        client.token, client.id)
    bot.send_message(message.chat.id,f'''
━━━━━━━━
Account Information
━━━━━━━━


#️⃣  Account ID {accountmetadata['id']}
🧑‍🦱  Display Name {accountmetadata['displayName']}
📧  Email {accountmetadata['email']}
🔐  Email Verified {accountmetadata['emailVerified']}
📛  Name {accountmetadata['name']}
📛  Last Name {accountmetadata['lastName']}
🌐  Country {accountmetadata['country']}
💰  VBucks Available {None}
🔒  2FA Enabled {accountmetadata['tfaEnabled']}
🕐  Last login {accountmetadata['lastLogin']}

🗺️  Current Season 
        Wins {cursesinfo[3]}
        Level {cursesinfo[1]}
        Purchased Battle Pass {cursesinfo[0]}
        Battle Pass Level {cursesinfo[2]}    
''')
    os.mkdir(message.from_user.username)
    print(client.token,client.id)
    seasonsinfoarr = list(seasonsinfo.keys())
    #seasonsinfoarr.reverse()
    bot.edit_message_text(
        f'checking seasons', msg.chat.id, msg.id)
    seasonstext=''
    for season in seasonsinfoarr:
        if seasonsinfo[season][1]==True:
            purchasedbp = '✅'
        else:
            purchasedbp = '❌'
        seasonstext+='| Season {}\n| Season Level: {}\n| Purchased Battle Pass: {}\n| Battle Pass Level: {}\n| Season Wins: {}\n\n'.format(season,
                                                        seasonsinfo[season][0],purchasedbp,seasonsinfo[season][2],seasonsinfo[season][3])
    bot.send_message(message.chat.id,seasonstext)
    msg = bot.send_message(message.chat.id,'making a picture of skins')
    for i in cosmetics_arrays:
        if i in WHITELIST:
            strtosend = f'making a picture of skins\n\n'
            for i1 in makeapickchecklist:
                strtosend += f'{i1}: {makeapickchecklist[i1]}\n'
            bot.edit_message_text(strtosend, msg.chat.id, msg.id)
            stuff.makeapic(
                cosmetics_name_and_info_arrays[i], '{}/{}.png'.format(message.from_user.username, i))
            makeapickchecklist[i] = '✅'

    photos = [open('{}/{}.png'.format(message.from_user.username, fn), 'rb')
              for fn in WHITELIST]
    media = [telebot.types.InputMediaPhoto(photo) for photo in photos]
    bot.send_media_group(msg.chat.id, media)
    bot.edit_message_text('here you go mate', msg.chat.id, msg.id)

    [i.close() for i in photos]
    print(client.token,client.id)
    shutil.rmtree(message.from_user.username)


if __name__ == '__main__':
    bot.infinity_polling()
    # try:

    #     client = auth.main(code)
    #     print(client.id)
    #     print(client.token)
    #     cosmetics_arrays, cosmetics_name_and_info_arrays = checkers.locker(
    #         '6ab5ba2b72f74083a64f559f59d5984b', '6af0265ecf8e41c08ca90a61d6768c00')
    #     for i in cosmetics_arrays:
    #         if i in WHITELIST:
    #             stuff.makeapic(
    #                 cosmetics_name_and_info_arrays[i], '{}.png'.format(i))
    # except Exception as e:
    #     print(e)
