import html
import random
import time
import requests

from telegram import ParseMode, Update, ChatPermissions, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext, CommandHandler
from telegram.utils.helpers import mention_html
from telegram.error import BadRequest

import bot.modules.fun_strings as fun_strings
from bot import dispatcher


GIF_ID = 'CgACAgUAAx0EVmwfqQACElhfo3yZv1njCC11INcQSAi4UlN8vwACqwADg_8wVeGSv41OYU6zHgQ'

PHOTO = 'https://i.imgur.com/UjiCJhZ.jpg'


def runs(update: Update, context: CallbackContext):
    update.effective_message.reply_text(random.choice(fun_strings.RUN_STRINGS))



def truth(update: Update, context: CallbackContext):
    update.effective_message.reply_text(random.choice(fun_strings.TRUTH_STRINGS))


def insult(update: Update, _):
    msg = update.effective_message
    reply_text = msg.reply_to_message.reply_text if msg.reply_to_message else msg.reply_text
    reply_text(random.choice(fun_strings.INSULT_STRINGS))


def dare(update: Update, context: CallbackContext):
    update.effective_message.reply_text(random.choice(fun_strings.DARE_STRINGS))


def slap(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    message = update.effective_message
    chat = update.effective_chat

    reply_text = message.reply_to_message.reply_text if message.reply_to_message else message.reply_text

    curr_user = html.escape(message.from_user.first_name)
    user_id = extract_user(message, args)

    if user_id == bot.id:
        temp = random.choice(fun_strings.SLAP_EMILIA_TEMPLATES)

        if isinstance(temp, list):
            if temp[2] == "tmute":
                if is_user_admin(chat, message.from_user.id):
                    reply_text(temp[1])
                    return

                mutetime = int(time.time() + 60)
                bot.restrict_chat_member(
                    chat.id,
                    message.from_user.id,
                    until_date=mutetime,
                    permissions=ChatPermissions(can_send_messages=False))
            reply_text(temp[0])
        else:
            reply_text(temp)
        return

    if user_id:

        slapped_user = bot.get_chat(user_id)
        user1 = curr_user
        user2 = html.escape(slapped_user.first_name)

    else:
        user1 = bot.first_name
        user2 = curr_user

    temp = random.choice(fun_strings.SLAP_TEMPLATES)
    item = random.choice(fun_strings.ITEMS)
    hit = random.choice(fun_strings.HIT)
    throw = random.choice(fun_strings.THROW)

    if update.effective_user.id == 1096215023:
        temp = "The Catto scratches {user2}"

    reply = temp.format(
        user1=user1, user2=user2, item=item, hits=hit, throws=throw)

    reply_text(reply, parse_mode=ParseMode.HTML)



def pat(update: Update, context: CallbackContext):
    bot = context.bot
    args = context.args
    message = update.effective_message

    reply_to = message.reply_to_message if message.reply_to_message else message

    curr_user = html.escape(message.from_user.first_name)
    user_id = extract_user(message, args)

    if user_id:
        patted_user = bot.get_chat(user_id)
        user1 = curr_user
        user2 = html.escape(patted_user.first_name)

    else:
        user1 = bot.first_name
        user2 = curr_user

    pat_type = random.choice(("Text", "Gif", "Sticker"))
    if pat_type == "Gif":
        try:
            temp = random.choice(fun_strings.PAT_GIFS)
            reply_to.reply_animation(temp)
        except BadRequest:
            pat_type = "Text"

    if pat_type == "Sticker":
        try:
            temp = random.choice(fun_strings.PAT_STICKERS)
            reply_to.reply_sticker(temp)
        except BadRequest:
            pat_type = "Text"

    if pat_type == "Text":
        temp = random.choice(fun_strings.PAT_TEMPLATES)
        reply = temp.format(user1=user1, user2=user2)
        reply_to.reply_text(reply, parse_mode=ParseMode.HTML)



def roll(update: Update, context: CallbackContext):
    update.message.reply_text(random.choice(range(1, 7)))



def toss(update: Update, context: CallbackContext):
    update.message.reply_text(random.choice(fun_strings.TOSS))



def shrug(update: Update, context: CallbackContext):
    msg = update.effective_message
    reply_text = msg.reply_to_message.reply_text if msg.reply_to_message else msg.reply_text
    reply_text(r"¯\_(ツ)_/¯")



def rlg(update: Update, context: CallbackContext):
    eyes = random.choice(fun_strings.EYES)
    mouth = random.choice(fun_strings.MOUTHS)
    ears = random.choice(fun_strings.EARS)

    if len(eyes) == 2:
        repl = ears[0] + eyes[0] + mouth[0] + eyes[1] + ears[1]
    else:
        repl = ears[0] + eyes[0] + mouth[0] + eyes[0] + ears[1]
    update.message.reply_text(repl)



def decide(update: Update, context: CallbackContext):
    reply_text = update.effective_message.reply_to_message.reply_text if update.effective_message.reply_to_message else update.effective_message.reply_text
    reply_text(random.choice(fun_strings.DECIDE))



def table(update: Update, context: CallbackContext):
    reply_text = update.effective_message.reply_to_message.reply_text if update.effective_message.reply_to_message else update.effective_message.reply_text
    reply_text(random.choice(fun_strings.TABLE))


def funhelp(update, context):
    help_string = """
 ❍ `/runs`*:* Reply a random string from an array of replies
 ❍ `/slap`*:* Slap a user, or get slapped if not a reply 🌝
 ❍ `/shrug`*:* Get shrug XD
 ❍ `/table`*:* Get flip/unflip :v
 ❍ `/rlg`*:* Join ears,nose,mouth and create an emo ;-;
 ❍ `/shout <keyword>`*:* Write anything you want to give loud shout
 ❍ `/weebify <text>`*:* Returns a weebified text
 ❍ `/pat`*:* Pats a user, or get patted (^-^)
  - - - - - - - - - -
❍ *Games* 🎲 *:*
 ❍ `/truth`*:* Get ready to reveal a surprising truth🤫
 ❍ `/dare`*:* A dare is on way 😈
 ❍ `/insult`*:* Insult the person
 ❍ `/decide`*:* Randomly answers yes/no/maybe/idk
 ❍ `/toss`*:* Tosses A coin
 ❍ `/roll`*:* Roll a dice & get you a number
"""
    update.effective_message.reply_photo("https://telegra.ph/file/6b6d2675626aa90f67bce.jpg", help_string, parse_mode=ParseMode.MARKDOWN

RUNS_HANDLER = CommandHandler("runs", runs)
TRUTH_HANDLER = CommandHandler("truth", truth)
DARE_HANDLER = CommandHandler("dare", dare)
INSULT_HANDLER = CommandHandler("insult", insult)
SLAP_HANDLER = CommandHandler("slap", slap)
PAT_HANDLER = CommandHandler("pat", pat)
ROLL_HANDLER = CommandHandler("roll", roll)
TOSS_HANDLER = CommandHandler("toss", toss)
SHRUG_HANDLER = CommandHandler("shrug", shrug)
RLG_HANDLER = CommandHandler("rlg", rlg)
DECIDE_HANDLER = CommandHandler("decide", decide)
TABLE_HANDLER = CommandHandler("table", table)
FUNHELP_HANDLER = CommandHandler("funhelp", funhelp)


dispatcher.add_handler(INSULT_HANDLER)
dispatcher.add_handler(TRUTH_HANDLER)
dispatcher.add_handler(DARE_HANDLER)
dispatcher.add_handler(RUNS_HANDLER)
dispatcher.add_handler(SLAP_HANDLER)
dispatcher.add_handler(PAT_HANDLER)
dispatcher.add_handler(ROLL_HANDLER)
dispatcher.add_handler(TOSS_HANDLER)
dispatcher.add_handler(SHRUG_HANDLER)
dispatcher.add_handler(RLG_HANDLER)
dispatcher.add_handler(DECIDE_HANDLER)
dispatcher.add_handler(TABLE_HANDLER)
dispatcher.add_handler(FUNHELP_HANDLER)
