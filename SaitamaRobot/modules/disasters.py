import html
import json
import os
from typing import Optional

from SaitamaRobot import (
    DEV_USERS,
    OWNER_USERID,
    DRAGONS,
    SUPPORT_CHAT,
    dispatcher,
)
from SaitamaRobot.modules.helper_funcs.chat_status import (
    dev_plus,
    sudo_plus,
    whitelist_plus,
)
from SaitamaRobot.modules.helper_funcs.extraction import extract_user
from SaitamaRobot.modules.log_channel import gloggable
from telegram import ParseMode, TelegramError, Update
from telegram.ext import CallbackContext, CommandHandler
from telegram.utils.helpers import mention_html

# TODO: fix addsudo and removesudo


def check_user_id(user_id: int, context: CallbackContext) -> Optional[str]:
    bot = context.bot
    if not user_id:
        reply = "That...is a chat! baka ka omae?"

    elif user_id == bot.id:
        reply = "This does not work that way."

    else:
        reply = None
    return reply


# This can serve as a deeplink example.
# disasters =
# """ Text here """

# do not async, not a handler
# def send_disasters(update):
#    update.effective_message.reply_text(
#        disasters, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

### Deep link example ends


# @dev_plus
# @gloggable
# def addsudo(update: Update, context: CallbackContext) -> str:
#    message = update.effective_message
#    user = update.effective_user
#    chat = update.effective_chat
#    bot, args = context.bot, context.args
#    user_id = extract_user(message, args)
#    user_member = bot.getChat(user_id)
#    rt = ""
#
#    reply = check_user_id(user_id, bot)
#    if reply:
#        message.reply_text(reply)
#        return ""
#
#    with open(ELEVATED_USERS_FILE, "r") as infile:
#        data = json.load(infile)
#
#    if user_id in DRAGONS:
#        message.reply_text("This member is already a Dragon Disaster")
#        return ""
#
#    data["sudos"].append(user_id)
#    DRAGONS.append(user_id)
#
#    with open(ELEVATED_USERS_FILE, "w") as outfile:
#        json.dump(data, outfile, indent=4)
#
#    update.effective_message.reply_text(
#        rt
#        + "\nSuccessfully set Disaster level of {} to Dragon!".format(
#            user_member.first_name,
#        ),
#    )
#
#    log_message = (
#        f"#SUDO\n"
#        f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
#        f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
#    )
#
#    if chat.type != "private":
#        log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message
#
#    return log_message
#
#
# @dev_plus
# @gloggable
# def removesudo(update: Update, context: CallbackContext) -> str:
#    message = update.effective_message
#    user = update.effective_user
#    chat = update.effective_chat
#    bot, args = context.bot, context.args
#    user_id = extract_user(message, args)
#    user_member = bot.getChat(user_id)
#
#    reply = check_user_id(user_id, bot)
#    if reply:
#        message.reply_text(reply)
#        return ""
#
#    with open(ELEVATED_USERS_FILE, "r") as infile:
#        data = json.load(infile)
#
#    if user_id in DRAGONS:
#        message.reply_text("Requested HA to demote this user to Civilian")
#        DRAGONS.remove(user_id)
#        data["sudos"].remove(user_id)
#
#        with open(ELEVATED_USERS_FILE, "w") as outfile:
#            json.dump(data, outfile, indent=4)
#
#        log_message = (
#            f"#UNSUDO\n"
#            f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
#            f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
#        )
#
#        if chat.type != "private":
#            log_message = "<b>{}:</b>\n".format(html.escape(chat.title)) + log_message
#
#        return log_message
#
#    else:
#        message.reply_text("This user is not a Dragon Disaster!")
#        return ""


@whitelist_plus
def sudolist(update: Update, context: CallbackContext):
    bot = context.bot
    true_sudo = DRAGONS
    reply = "<b>Known Dragon Disasters 🐉:</b>\n"
    for each_user in true_sudo:
        user_id = each_user
        try:
            user = bot.get_chat(user_id)
            reply += f"• {mention_html(user_id, html.escape(user.first_name))}\n"
        except TelegramError:
            pass
    update.effective_message.reply_text(reply, parse_mode=ParseMode.HTML)


@whitelist_plus
def devlist(update: Update, context: CallbackContext):
    bot = context.bot
    true_dev = set(DEV_USERS).difference({OWNER_USERID})
    reply = "<b>Hero Association Members ⚡️:</b>\n"
    for each_user in true_dev:
        user_id = each_user
        try:
            user = bot.get_chat(user_id)
            reply += f"• {mention_html(user_id, html.escape(user.first_name))}\n"
        except TelegramError:
            pass
    update.effective_message.reply_text(reply, parse_mode=ParseMode.HTML)


__help__ = f"""
*⚠️ Notice:*
Commands listed here only work for users with special access and are mainly used for troubleshooting, debugging purposes.
Group admins/group owners do not need these commands.

 ╔ *List all special users:*
 ╠ `/dragons`*:* Lists all Dragon disasters
 ╠ `/demons`*:* Lists all Demon disasters
 ╠ `/tigers`*:* Lists all Tigers disasters
 ╠ `/wolves`*:* Lists all Wolf disasters
 ╠ `/heroes`*:* Lists all Hero Association members
 ╠ `/adddragon`*:* Adds a user to Dragon
 ╚ `Add dev doesnt exist, devs should know how to add themselves`

 ╔ *Ping:*
 ╠ `/ping`*:* gets ping time of bot to telegram server
 ╚ `/pingall`*:* gets all listed ping times

 ╔ *Broadcast: (Bot owner only)*
 ╠  *Note:* This supports basic markdown
 ╠ `/broadcastall`*:* Broadcasts everywhere
 ╠ `/broadcastusers`*:* Broadcasts too all users
 ╚ `/broadcastgroups`*:* Broadcasts too all groups

 ╔ *Groups Info:*
 ╠ `/groups`*:* List the groups with Name, ID, members count as a txt
 ╠ `/leave <ID>`*:* Leave the group, ID must have hyphen
 ╠ `/stats`*:* Shows overall bot stats
 ╠ `/getchats`*:* Gets a list of group names the user has been seen in. Bot owner only
 ╚ `/ginfo username/link/ID`*:* Pulls info panel for entire group

 ╔ *Access control:*
 ╠ `/ignore`*:* Blacklists a user from
 ╠  using the bot entirely
 ╠ `/lockdown <off/on>`*:* Toggles bot adding to groups
 ╠ `/notice`*:* Removes user from blacklist
 ╚ `/ignoredlist`*:* Lists ignored users

 ╔ *Module loading:*
 ╠ `/listmodules`*:* Prints modules and their names
 ╠ `/unload <name>`*:* Unloads module dynamically
 ╚ `/load <name>`*:* Loads module

 ╔ *Speedtest:*
 ╚ `/speedtest`*:* Runs a speedtest and gives you 2 options to choose from, text or image output

 ╔ *Module loading:*
 ╠ `/listmodules`*:* Lists names of all modules
 ╠ `/load modulename`*:* Loads the said module to
 ╠   memory without restarting.
 ╠ `/unload modulename`*:* Loads the said module from
 ╚   memory without restarting.memory without restarting the bot

 ╔ *Remote commands:*
 ╠ `/rban user group`*:* Remote ban
 ╠ `/runban user group`*:* Remote un-ban
 ╠ `/rpunch user group`*:* Remote punch
 ╠ `/rmute user group`*:* Remote mute
 ╚ `/runmute user group`*:* Remote un-mute

 ╔ *Debugging and Shell:*
 ╠ `/debug <on/off>`*:* Logs commands to updates.txt
 ╠ `/logs`*:* Run this in support group to get logs in pm
 ╠ `/eval`*:* Self explanatory
 ╠ `/sh`*:* Runs shell command
 ╠ `/shell`*:* Runs shell command
 ╠ `/clearlocals`*:* As the name goes
 ╠ `/dbcleanup`*:* Removes deleted accs and groups from db
 ╚ `/py`*:* Runs python code
 


Visit @{SUPPORT_CHAT} for more information.
"""

# SUDO_HANDLER = CommandHandler(("addsudo", "adddragon"), addsudo, run_async=True)
# UNSUDO_HANDLER = CommandHandler(
#    ("removesudo", "removedragon"), removesudo, run_async=True
# )
SUDOLIST_HANDLER = CommandHandler(["sudolist", "dragons"], sudolist, run_async=True)
DEVLIST_HANDLER = CommandHandler(["devlist", "heroes"], devlist, run_async=True)

# dispatcher.add_handler(SUDO_HANDLER)
# dispatcher.add_handler(UNSUDO_HANDLER)
dispatcher.add_handler(SUDOLIST_HANDLER)
dispatcher.add_handler(DEVLIST_HANDLER)

__mod_name__ = "Disasters"
__handlers__ = [
    #   SUDO_HANDLER,
    #   UNSUDO_HANDLER,
    SUDOLIST_HANDLER,
    DEVLIST_HANDLER,
]
