import os
import requests
import aiohttp
import youtube_dl

from pyrogram import filters
from bot import app
from youtube_search import YoutubeSearch
from telegram.ext import CommandHandler
from bot import dispatcher

def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))


@app.on_message(filters.command(['song']))
def song(client, message):

    user_id = message.from_user.id 
    user_name = message.from_user.first_name 
    rpk = "["+user_name+"](tg://user?id="+str(user_id)+")"

    query = ''
    for i in message.command[1:]:
        query += ' ' + str(i)
    print(query)
    m = message.reply('🔎 𝑴𝒆𝒏𝒄𝒂𝒓𝒊 𝒎𝒖𝒔𝒊𝒌...')
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        #print(results)
        title = results[0]["title"][:40]       
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f'thumb{title}.jpg'
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, 'wb').write(thumb.content)


        duration = results[0]["duration"]
        url_suffix = results[0]["url_suffix"]
        views = results[0]["views"]

    except Exception as e:
        m.edit(
            "😌 Tidak menemukan apa-apa. Maaf.\n\nCoba kalimat lain atau mungkin mengejanya dengan benar."
        )
        print(str(e))
        return
    m.edit("`𝑴𝒆𝒏𝒅𝒐𝒘𝒏𝒍𝒐𝒂𝒅 𝒎𝒖𝒔𝒊𝒌... 𝒔𝒂𝒃𝒂𝒓 𝒚𝒂😅 `")
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = f'🎙 **𝐉𝐮𝐝𝐮𝐥**: [{title[:35]}]({link})\n🎬 **𝐒𝐮𝐦𝐛𝐞𝐫**: YouTube\n⏱️ **𝐃𝐮𝐫𝐚𝐬𝐢**: `{duration}`\n👁‍🗨 **𝐃𝐢𝐭𝐨𝐧𝐭𝐨𝐧**: `{views}`\n🤖 **𝐁𝐲**: @MirroringV3Bot '
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        message.reply_audio(audio_file, caption=rep, thumb=thumb_name, parse_mode='md', title=title, duration=dur)
        m.delete()
    except Exception as e:
        m.edit('An error Occured! \nReport to @OdierBambi')
        print(e)

    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)


SONG_HANDLER = CommandHandler("song", song)

dispatcher.add_handler(SONG_HANDLER)
