import html
import time
import datetime
import requests, logging
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from telegram import Message, Chat, Update, Bot, MessageEntity
from bot import dispatcher, OWNER_ID, SUDO_USERS
from telegram import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton

count = 0
def music(bot: Bot, update: Update):
	message = update.effective_message
	global count

	chatId = update.message.chat_id
    
	video_id = ''.join

	if video_id.find('youtu.be') != -1:
		index = video_id.rfind('/') + 1
		video_id = video_id[index:][:11]
		message.reply_text("Please wait...\ndownloading audio.")

	elif video_id.find('youtube') != -1:
		index = video_id.rfind('?v=') + 3
		video_id = video_id[index:][:11]
		message.reply_text("Please wait...\downloading audio.")

	elif not video_id.find('youtube') != -1:
		message.reply_text("Please provide me youtube link")

	elif not video_id.find('youtu.be') != -1:
		message.reply_text("Please provide me youtube link")
		

        



	r = requests.get(f'https://api.pointmp3.com/dl/{video_id}?format=mp3')
	

	json1_response = r.json()

	if not json1_response['error']:
		

		redirect_link = json1_response['url']

		r = requests.get(redirect_link)
		

		json2_response = r.json()

		if not json2_response['error']:
			payload = json2_response['payload']

			info = '*{0}* \nUploaded by @AnonymousD3061'.format(payload['fulltitle'])

			try:
				
				bot.send_audio(chat_id=chatId, audio=json2_response['url'] ,parse_mode='Markdown',text="meanya", caption=info)
				count += 1
				print("\033[1m\033[96m" + "Download count: " + str(count) + "\033[0m")
			except:
				bot.send_message(chat_id=chatId, text='Something went wrong with the download..!\nPlease Report there @AnonymousD3061')


MUSIC_HANDLER = CommandHandler('music', music)
dispatcher.add_handler(MUSIC_HANDLER)
